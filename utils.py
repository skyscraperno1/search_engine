import re

def process_content(content):
    # 去掉 <span> 标签及其内容
    content_no_span = re.sub(r'<span.*?</span>', '', content, flags=re.DOTALL)

    # 找到第一个“·”的位置
    dot_index = content_no_span.find('·')

    # 如果找到了“·”，去掉它前面的所有内容
    if dot_index != -1:
        content_no_span = content_no_span[dot_index + 1:]

    # 去掉所有 HTML 标签
    final_content = re.sub(r'<.*?>', '', content_no_span).strip()

    return final_content
