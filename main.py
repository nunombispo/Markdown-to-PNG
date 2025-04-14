from markdown import markdown
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time


def markdown_to_png(md_path, output_path='output.png'):
    """
    Convert a markdown file to a PNG image.
    
    Args:
        md_path (str): Path to the markdown file
        output_path (str): Path where the PNG will be saved
    """
    try:
        # Convert markdown to HTML
        md_text = Path(md_path).read_text()
        html_body = markdown(md_text, extensions=['tables', 'fenced_code'])

        # HTML template with styling
        html_template = """
        <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
            <script>hljs.highlightAll();</script>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                    padding: 40px;
                    max-width: 800px;
                    margin: auto;
                    background: white;
                    line-height: 1.6;
                    color: #24292e;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin: 16px 0;
                    font-size: 14px;
                }
                th, td {
                    border: 1px solid #e1e4e8;
                    padding: 8px 16px;
                    text-align: left;
                }
                th {
                    background-color: #f6f8fa;
                    font-weight: 600;
                }
                tr:nth-child(even) {
                    background-color: #fafbfc;
                }
                tr:hover {
                    background-color: #f6f8fa;
                }
                pre {
                    background: #f6f8fa;
                    border-radius: 6px;
                    padding: 16px;
                    overflow: auto;
                    font-size: 14px;
                    line-height: 1.45;
                    margin: 16px 0;
                }
                code {
                    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
                    font-size: 85%;
                }
                pre code {
                    padding: 0;
                    background: transparent;
                }
                h1 {
                    font-size: 2em;
                    padding-bottom: 0.3em;
                    border-bottom: 1px solid #eaecef;
                }
            </style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

        # Create full HTML
        full_html = html_template.replace("{content}", html_body)

        # Save to temporary file
        temp_html = "temp.html"
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(full_html)

        # Configure Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1000,800")
        chrome_options.add_argument("--hide-scrollbars")
        
        # Initialize Chrome and take screenshot
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(f"file://{os.path.abspath(temp_html)}")
            time.sleep(1)  # Wait for rendering
            driver.save_screenshot(output_path)
            
            if os.path.exists(output_path):
                print(f"Successfully saved PNG to {output_path}")
            else:
                print("Failed to create output file")
                
        finally:
            driver.quit()
            if os.path.exists(temp_html):
                os.remove(temp_html)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return


if __name__ == "__main__":
    markdown_to_png('example.md', 'example_output.png')
