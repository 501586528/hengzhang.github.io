import os
import json
import re
from datetime import datetime

blogs_dir = os.path.join(os.path.dirname(__file__), 'blogs')
output_file = os.path.join(os.path.dirname(__file__), 'blogs.json')

articles = []

for filename in os.listdir(blogs_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(blogs_dir, filename)
        
        # 提取Markdown标题
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^#\s+(.+?)\s*$', content, re.MULTILINE)
            title = match.group(1).strip() if match else os.path.splitext(filename)[0]
        
        # 获取文件创建时间
        created_at = datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
        
        # 提取前100字作为摘要
        excerpt = re.sub(r'[#*_\-`]', '', content.split('\n\n')[1] if '\n\n' in content else content[:100]).strip()
        
        articles.append({
            'filename': filename,
            'title': title,
            'created_at': created_at,
            'url': f'/blogs/{filename}',
            'excerpt': excerpt
        })

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f'Generated {output_file} with {len(articles)} articles.')