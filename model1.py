import datasets
import pandas as pd
from fastai.text.all import *
from transformers import *
from blurr.data.all import *
from blurr.modeling.all import *

class model:
	modelLoad = None

	def __init__(self):
		pretrained_model_name = "facebook/bart-large-cnn"
		hf_arch, hf_config, hf_tokenizer, hf_model = BLURR.get_hf_objects(pretrained_model_name,
																		  model_cls=BartForConditionalGeneration)
		model = HF_BaseModelWrapper(hf_model)
		learn_cbs = [HF_BaseModelCallback]
		df = pd.read_csv("C:/Manthan/news_summary_train_small.csv")
		df = df.drop(['Unnamed: 0'], axis=1)
		text_gen_kwargs = default_text_gen_kwargs(hf_config, hf_model, task='summarization')
		hf_batch_tfm = HF_Seq2SeqBeforeBatchTransform(hf_arch, hf_config, hf_tokenizer, hf_model,
													  max_length=256, max_tgt_length=130,
													  text_gen_kwargs=text_gen_kwargs)
		blocks = (HF_Seq2SeqBlock(before_batch_tfm=hf_batch_tfm), noop)
		dblock = DataBlock(blocks=blocks, get_x=ColReader('article'), get_y=ColReader('highlights'),
						   splitter=RandomSplitter())

		df = df.rename(columns={'Summary': 'highlights', 'Text': 'article'})
		dls = dblock.dataloaders(df, bs=2)
		dls.show_batch(dataloaders=dls, max_n=2)
		seq2seq_metrics = {
			'rouge': {
				'compute_kwargs': {'rouge_types': ["rouge1", "rouge2", "rougeL"], 'use_stemmer': True},
				'returns': ["rouge1", "rouge2", "rougeL"]
			},
			'bertscore': {
				'compute_kwargs': {'lang': 'en'},
				'returns': ["precision", "recall", "f1"]
			}
		}
		fit_cbs = [HF_Seq2SeqMetricsCallback(custom_metrics=seq2seq_metrics)]
		learn = Learner(dls,
						model,
						opt_func=ranger,
						loss_func=CrossEntropyLossFlat(),
						cbs=learn_cbs,
						splitter=partial(seq2seq_splitter, arch=hf_arch)).to_fp16()
		self.modelLoad = learn.load("C:/Manthan/summarize_export")

	def summarize(self, text):
		outputs = self.modelLoad.blurr_generate(text, early_stopping=True, num_beams=4, num_return_sequences=1)
		for idx, o in enumerate(outputs):
			return o

# test_article = """
#         The past 12 months have been the worst for aviation fatalities so far this decade - with the total of number of people killed if airline
#         crashes reaching 1,050 even before the Air Asia plane vanished. Two incidents involving Malaysia Airlines planes - one over eastern Ukraine and the other in the Indian Ocean - led to the deaths of 537 people, while an Air Algerie crash in Mali killed 116 and TransAsia Airways crash in Taiwan killed a further 49 people. The remaining 456 fatalities were largely in incidents involving small commercial planes or private aircraft operating on behalf of companies, governments or organisations. Despite 2014 having the highest number of fatalities so far this decade, the total number of crashes was in fact the lowest since the first commercial jet airliner took off in 1949 - totalling just 111 across the whole world over the past 12 months. The all-time deadliest year for aviation was 1972 when a staggering 2,429 people were killed in a total of 55 plane crashes - including the crash of Aeroflot Flight 217, which killed 174 people in Russia, and Convair 990 Coronado, which claimed 155 lives in Spain. However this year's total death count of 1,212, including those presumed dead on board the missing Air Asia flight, marks a significant rise on the very low 265 fatalities in 2013 - which led to it being named the safest year in aviation since the end of the Second World War. Scroll down for videos. Deadly: The past 12 months have been the worst for aviation fatalities so far this decade - with the total of number of people killed if airline crashes reaching 1,158 even before the Air Asia plane (pictured) vanished. Fatal: Two incidents involving Malaysia Airlines planes - one over eastern Ukraine (pictured) and the other in the Indian Ocean - led to the deaths of 537 people. Surprising: Despite 2014 having the highest number of fatalities so far this decade, the total number of crashes was in fact the lowest since the first commercial jet airliner took off in 1949. 2014 has been a horrific year for Malaysia-based airlines, with 537 people dying on Malaysia Airlines planes, and a further 162 people missing and feared dead in this week's Air Asia incident. In total more than half the people killed in aviation incidents this year had been flying on board Malaysia-registered planes. In January a total of 12 people lost their lives in five separate incidents, while the same number of crashes in February killed 107.
#         """

# m = model()
# print(m.summarize())
