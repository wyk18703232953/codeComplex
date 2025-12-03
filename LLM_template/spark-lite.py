from openai import OpenAI
client = OpenAI(
        api_key="GnZpLRUqXACfasNtdRzM:DOmdLvpitzquFcnIXimk", 
        base_url = 'https://spark-api-open.xf-yun.com/v1' # 指向讯飞星火的请求地址
    )
completion = client.chat.completions.create(
    model='lite', # 指定请求的版本
    messages=[
        {
            "role": "user",
            "content": '''
            程序员的困惑\n\n\n“我不明白，为什么我 们的程序不能运行？” 一位程序员向经理抱怨道。\n\n“你要知道，”经理回答说，“这是一台洗衣机。”希望你喜欢这个笑话 哦！
            这个笑话搞笑在哪儿？
            '''
        }
    ]
)
print(completion.choices[0].message)