"""
基于 chinese-roberta-wwm-ext 微调训练 6 分类情感分析模型: https://blog.csdn.net/qq_43692950/article/details/131792392
Chinese-BERT-wwm 安装和配置指南: https://blog.csdn.net/gitblog_09456/article/details/142225586


"""

# from transformers import BertTokenizer, BertModel
# path = './chinese-bert-wwm-ext'
# # 加载分词器
# tokenizer = BertTokenizer.from_pretrained(path)
#
# # 加载模型
# model = BertModel.from_pretrained(path)
#
# # 示例文本
# text = "使用语言模型来预测下一个词的probability"
#
# # 分词
# inputs = tokenizer(text, return_tensors="pt")
#
# # 模型推理
# outputs = model(**inputs)
#
# # 输出结果
# last_hidden_states = outputs.last_hidden_state
# print(last_hidden_states)


from transformers import BertModel, BertTokenizer

# 加载预训练模型和分词器
model = BertModel.from_pretrained('../chinese-bert-wwm-ext')
tokenizer = BertTokenizer.from_pretrained('../chinese-bert-wwm-ext')

# 准备输入文本
text = "你好，世界"
inputs = tokenizer(text, return_tensors='pt')

# 获取模型输出
outputs = model(**inputs)

# 输出最后一层隐藏状态
last_hidden_states = outputs.last_hidden_state
print(last_hidden_states)

# 如果你还想获得池化输出，可以直接访问outputs.pooler_output
pooled_output = outputs.pooler_output
print(pooled_output)
