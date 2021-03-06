# -*- coding: utf-8 -*-
"""AbstractiveTextSummarization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R9yjxHR2OiFr-62qgu9zNQnCFZBawTrc
"""

!pip install ohmeow-blurr -q
!pip install datasets -q
!pip install bert-score -q

import datasets
import pandas as pd
from fastai.text.all import *
from transformers import *

from blurr.data.all import *
from blurr.modeling.all import *

raw_data = datasets.load_dataset('cnn_dailymail', '3.0.0')

"""Data Preprocessing"""

df = pd.DataFrame(raw_data["train"])

pretrained_model_name = "facebook/bart-large"
hf_arch, hf_config, hf_tokenizer, hf_model = BLURR.get_hf_objects(pretrained_model_name, 
                                                                  model_cls=BartForConditionalGeneration)

hf_arch, type(hf_config), type(hf_tokenizer), type(hf_model)

df.shape, df.columns

df.drop(columns = "id", inplace = True)

art_lengths = []
summ_lengths = []
for i in range(0, len(df)):
  art_l = len(df.iloc[i, 0].split(" "))
  sum_l = len(df.iloc[i, 1].split(" "))
  art_lengths.append(art_l)
  summ_lengths.append(sum_l)

len(art_lengths), len(summ_lengths)

import seaborn as sns
sns.distplot(pd.Series(art_lengths), kde = True)

sns.distplot(pd.Series(summ_lengths), kde = True)

pd.concat([pd.Series(summ_lengths), pd.Series(art_lengths)], axis = 1, keys = ["Summary", "Article"]).describe()

df.drop(df[df["article"].map(lambda s : len(s.split())) > 1024].index, inplace = True)

df.shape

text_gen_kwargs = default_text_gen_kwargs(hf_config, hf_model, task='summarization'); 
text_gen_kwargs

"""Loading Model"""

hf_batch_tfm = HF_Seq2SeqBeforeBatchTransform(hf_arch, hf_config, hf_tokenizer, hf_model, 
                                              max_length=256, max_tgt_length=130, text_gen_kwargs=text_gen_kwargs)

blocks = (HF_Seq2SeqBlock(before_batch_tfm=hf_batch_tfm), noop)

dblock = DataBlock(blocks=blocks, get_x=ColReader('article'), get_y=ColReader('highlights'), splitter=RandomSplitter())

df = df.rename(columns={'Summary': 'highlights', 'Text': 'article'})
dls = dblock.dataloaders(df, bs=2)

len(dls.train.items), len(dls.valid.items)

b = dls.one_batch()
len(b), b[0]['input_ids'].shape, b[1].shape

dls.show_batch(dataloaders=dls, max_n=2)

seq2seq_metrics = {
        'rouge': {
            'compute_kwargs': { 'rouge_types': ["rouge1", "rouge2", "rougeL"], 'use_stemmer': True },
            'returns': ["rouge1", "rouge2", "rougeL"]
        },
        'bertscore': {
            'compute_kwargs': { 'lang': 'en' },
            'returns': ["precision", "recall", "f1"]
        }
    }

model = HF_BaseModelWrapper(hf_model)
learn_cbs = [HF_BaseModelCallback]
fit_cbs = [HF_Seq2SeqMetricsCallback(custom_metrics=seq2seq_metrics)]

learn = Learner(dls, 
                model,
                opt_func=ranger,
                loss_func=CrossEntropyLossFlat(),
                cbs=learn_cbs,
                splitter=partial(seq2seq_splitter, arch=hf_arch)).to_fp16()

learn.create_opt() 
learn.freeze()

"""Finding Learning Rate"""

learn.lr_find()

b = dls.one_batch()
preds = learn.model(b[0])
len(preds),preds[0], preds[1].shape

"""Training Model"""

learn.fit_one_cycle(1, lr_max=3e-5, cbs=fit_cbs)

learn.show_results(learner=learn, max_n=2)

test_article = """
The past 12 months have been the worst for aviation fatalities so far this decade - with the total of number of people killed if airline 
crashes reaching 1,050 even before the Air Asia plane vanished. Two incidents involving Malaysia Airlines planes - one over eastern Ukraine and the other in the Indian Ocean - led to the deaths of 537 people, while an Air Algerie crash in Mali killed 116 and TransAsia Airways crash in Taiwan killed a further 49 people. The remaining 456 fatalities were largely in incidents involving small commercial planes or private aircraft operating on behalf of companies, governments or organisations. Despite 2014 having the highest number of fatalities so far this decade, the total number of crashes was in fact the lowest since the first commercial jet airliner took off in 1949 - totalling just 111 across the whole world over the past 12 months. The all-time deadliest year for aviation was 1972 when a staggering 2,429 people were killed in a total of 55 plane crashes - including the crash of Aeroflot Flight 217, which killed 174 people in Russia, and Convair 990 Coronado, which claimed 155 lives in Spain. However this year's total death count of 1,212, including those presumed dead on board the missing Air Asia flight, marks a significant rise on the very low 265 fatalities in 2013 - which led to it being named the safest year in aviation since the end of the Second World War. Scroll down for videos. Deadly: The past 12 months have been the worst for aviation fatalities so far this decade - with the total of number of people killed if airline crashes reaching 1,158 even before the Air Asia plane (pictured) vanished. Fatal: Two incidents involving Malaysia Airlines planes - one over eastern Ukraine (pictured) and the other in the Indian Ocean - led to the deaths of 537 people. Surprising: Despite 2014 having the highest number of fatalities so far this decade, the total number of crashes was in fact the lowest since the first commercial jet airliner took off in 1949. 2014 has been a horrific year for Malaysia-based airlines, with 537 people dying on Malaysia Airlines planes, and a further 162 people missing and feared dead in this week's Air Asia incident. In total more than half the people killed in aviation incidents this year had been flying on board Malaysia-registered planes. In January a total of 12 people lost their lives in five separate incidents, while the same number of crashes in February killed 107. 
"""

test_article2 = """US-based private equity firm General Atlantic is in talks to invest about
    $850 million to $950 million in Reliance Industries' digital unit Jio
    Platforms, the Bloomberg reported. Saudi Arabia's $320 billion sovereign
    wealth fund is reportedly also exploring a potential investment in the
    Mukesh Ambani-led company. The 'Public Investment Fund' is looking to
    acquire a minority stake in Jio Platforms"""

"""Evaluating"""

outputs = learn.blurr_generate(test_article2, early_stopping=True, num_beams=4, num_return_sequences=1)

for idx, o in enumerate(outputs):
    print(f'=== Prediction {idx+1} ===\n{o}\n')

stop

"""Saving"""

export_fname = 'summarize_export'
learn.metrics = None
#learn.save(fname=f'{export_fname}.pkl')
learn.save(f'{export_fname}', with_opt=False)