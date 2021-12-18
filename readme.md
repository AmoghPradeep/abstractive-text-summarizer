# Abstractive Text Summarizer
  <p align="center">
    <img src="https://user-images.githubusercontent.com/57984703/146382686-396e248c-54a7-4371-bea6-b52a74b51522.gif" alt="Transformers - Diagram" style= "width : 80%"/>
  </p>
  <p align="center">Summarizer UI</p>
 
© **Team Binary Brains** @ Manthan 2021 Hackathon<br>
- [Amogh Pradeep](https://www.linkedin.com/in/amogh-pradeep-0061b9108/)
- [Harshad Bhere](https://github.com/harshadbhere)
- [Harshvardhan Thakur](https://github.com/hvt0707)



## How to install ##
Steps : 
  1. Clone repository.
  2. Install dependencies using ```pip install -r requirements.txt```
  3. Run app.py using ```python app.py```

## Problem Overview : Extractive vs Abstractive Summarization
**Extraction-based Summarization:** <br>
The extractive approach involves picking up the most important phrases and lines from the documents. It then combines all the important lines to create the summary. So, in this case, every line and word of the summary actually belongs to the original document which is summarized. Extractive summaries can often be inconsistent grammatically, as sentences are stitched together haphazardly.

**Abstraction-based Summarization:** <br>
The abstractive approach involves summarization based on deep learning. So, it uses new phrases and terms, different from the actual document, while keeping the points the same, just like how we actually summarize. This results in a natural, grammatically accurate summary. This makes it much harder than the extractive approach. 

## Approach : Introducing Transformer Nueral Networks.
Text summarization is a complex NLP task which requires the model to retain the *context* of each word in the original article. <br> <br>
👉 The most simple way of achieving this is by using *Recurrent Neural Networks*. RNN's are a type of Neural Network where the output from the previous step is fed as input to the current step.
<p align="center">
  <img src="https://miro.medium.com/max/627/1*go8PHsPNbbV6qRiwpUQ5BQ.png" alt="RNN - Diagram"/>
</p>
But Recurrent Neural Networks suffer from short-term memory (read <a href="https://en.wikipedia.org/wiki/Vanishing_gradient_problem">Vanishing & Exploding gradient problem</a>). If a sequence is long enough, they’ll have a hard time carrying information from earlier time steps to later ones. This can be problematic while summarizing any news article.
<br>
<br>
👉 An improvement over RNN's are <b>LSTM and GRU</b>. LSTM ’s and GRU’s were created as the solution to short-term memory. They have internal mechanisms called gates that can regulate the flow of information.
<br>
<br>
<p align="center">
  <img src="https://user-images.githubusercontent.com/15166794/39033683-3020ce04-44ae-11e8-821f-1a9652ff5025.png" alt="LSTM - Diagram"/>
</p>
The problem with LSTM’s, is that they tend to have poor memory recall with data they’ve seen many time-steps ago, moreover these models are computationally intensive and their sequential nature prevents us from taking advantage of parallel computing.
<br>
<br>
👉 <b>Transformers based on Self-Attention </b> was first introduced in the  <a href="https://arxiv.org/abs/1706.03762"> Attention Is All You Need </a> paper by Ashish Vaswani et al. It is an improvement over Bahdanau's attention. In simple words it self-attention is a mechanism that allows each input in a sequence to look at the whole sequence to compute a representation of the sequence.
<br>
<br>
<p align="center">
  <img src="https://jalammar.github.io/images/t/transformer_self-attention_visualization_3.png" alt="Self Attention - Diagram"/>
</p>
<p align="center"> Calculating Self Attention for "it" </p>
<br>
<div>
This is implemented using a Transformer. A transformer consists of an <b>Encoder and a Decoder</b>. In simple terms, the encoder is responsible for calculating the self-attention and positional encoding. The decoder uses the output of the Encoder and the Outputs (shifted right) to generate the summary. Both Encoder and Decoder are composed of modules that can be stacked on top of each other multiple times.
    <p align="center">
      <img src="https://jalammar.github.io/images/t/The_transformer_encoders_decoders.png" alt="Transformers - Diagram" style= "width : 40%"/>
    </p>
    <p align="center">Transformer Architecture</p>
</div>
<br>
Transformers solve both the disadvantages of LSTM. They can recall data they've seen from anywhere in the input article, and we can also use parallel computing in many stages.

<h2> Implementation </h2>
<br>
👉 For the Model, we will use Transfer Learning with a NLP transformer - “bart-base” and train it on InShorts and CNN-DailyMail dataset. <br> <br>
    <p align="center">
      <img src="https://user-images.githubusercontent.com/57984703/145615462-05f6717f-8da6-4801-a84c-bc90512b3a98.JPG" alt="Workflow - Diagram" style = "width : 50%"/>
    </p>
    <p align="center"> Workflow </p>
<br>
👉 For the UI, we have used the Flask framework to connect our model with the front-end. We have used AJAX to enable server-client communications.
<br>
👉 We have also implemented support for summarizing links, documents and keywords provided by the user. We have used Scrapy and PyPDF2 to achieve this.

## Articles and Summary
<br>
<table>
    <tr style="text-align: center;">
        <th>Type</th>
        <th style="width: 300px;">Article</th>
        <th>Summary</th>
    </tr>
    <tr>
        <td style="text-align: center;">Link</td>
        <td><a href="https://en.wikipedia.org/wiki/Nico_Ditch">https://en.wikipedia.org/wiki/Nico_Ditch</a></td>
        <td>Nico Ditch is a six-mile (9.7 km) long linear earthwork between Ashton-under-Lyne and Stretford in Greater Manchester, England. It was dug as a defensive fortification, or possibly a boundary marker, between the 5th and 11th century. The ditch is still visible in short sections, such as a 330-yard (300 m) stretch in Denton Golf Course. Part of the earthwork is protected as a Scheduled Ancient Monument.</td>
    </tr>
    <tr>
        <td style="text-align: center;">Keyword</td>
        <td>U.S. Route 45 in Michigan</td>
        <td>US Highway 45 (US 45) is a highway that runs from Mobile, Alabama, to the Upper Peninsula (UP) of the state of Michigan. The highway forms a part of the Michigan trunkline highway system that is maintained by the Michigan Department of Transportation (MDOT) It enters the state from Wisconsin south of Watersmeet, ending at an intersection with Ontonagon Street in Ontario. In between, the roadway crosses the UP running for approximately 54+3⁄4 miles (88.1 km) through the Ottawa National Forest.</td>
    </tr>
    <tr>
        <td style="text-align: center;">Text</td>
        <td>The past 12 months have been the worst for aviation fatalities so far this decade - with the total of number of people killed if airline crashes reaching 1,050 even before the Air Asia plane vanished. Two incidents involving Malaysia Airlines planes - one over eastern Ukraine and the other in the Indian Ocean - led to the deaths of 537 people, while an Air Algerie crash in Mali killed 116 and TransAsia Airways crash in Taiwan killed a further 49 people. The remaining 456 fatalities were largely in incidents involving small commercial planes or private aircraft operating on behalf of companies, governments or organisations. Despite 2014 having the highest number of fatalities so far this decade, the total number of crashes was in fact the lowest since the first commercial jet airliner took off in 1949 - totalling just 111 across the whole world over the past 12 months. The all-time deadliest year for aviation was 1972 when a staggering 2,429 people were killed in a total of 55 plane crashes - including the crash of Aeroflot Flight 217, which killed 174 people in Russia, and Convair 990 Coronado, which claimed 155 lives in Spain. However this year's total death count of 1,212, including those presumed dead on board the missing Air Asia flight, marks a significant rise on the very low 265 fatalities in 2013 - which led to it being named the safest year in aviation since the end of the Second World War. Scroll down for videos. Deadly: The past 12 months have been the worst for aviation fatalities so far this decade - with the total of number of people killed if airline crashes reaching 1,158 even before the Air Asia plane (pictured) vanished. Fatal: Two incidents involving Malaysia Airlines planes - one over eastern Ukraine (pictured) and the other in the Indian Ocean - led to the deaths of 537 people. Surprising: Despite 2014 having the highest number of fatalities so far this decade, the total number of crashes was in fact the lowest since the first commercial jet airliner took off in 1949. 2014 has been a horrific year for Malaysia-based airlines, with 537 people dying on Malaysia Airlines planes, and a further 162 people missing and feared dead in this week's Air Asia incident. In total more than half the people killed in aviation incidents this year had been flying on board Malaysia-registered planes. In January a total of 12 people lost their lives in five separate incidents, while the same number of crashes in February killed 107.</td>
        <td>The past 12 months have been the worst for aviation fatalities so far this decade. The total number of people killed if airline crashes reached 1,050 even before Air Asia plane vanished. Two incidents involving Malaysia Airlines planes led to the deaths of 537 people in 2014. The remaining 456 fatalities were largely in incidents involving small commercial planes or private aircraft operating on behalf of companies, governments or organisations. Despite 2014 having the highest number of fatalities, the number of crashes was the lowest since the first commercial jet airliner took off in 1949.</td>
    </tr>
</table>
