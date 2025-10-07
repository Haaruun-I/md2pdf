import argparse, logging, os, pathlib, re, logging, builtins

from playwright.sync_api import sync_playwright
import tempfileServer
from markdown_it import MarkdownIt

from pygments import highlight
import pygments.lexers as lexers
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


# parts of this code shamelessly stolen(borrowed) from bellanda/markdown-html-pdf
def apply_syntax_highlighting(html_content):
    code_block_pattern = r'<pre><code class="language-(\w+)">(.*?)</code></pre>'

    def replace_code_block(match):
        lang = match.group(1)
        code = match.group(2)

        code = (
            code.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
        )

        formatter = HtmlFormatter(
            cssclass="highlight", noclasses=True
        )
        try:
            lexer = lexers.get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = lexers.guess_lexer(code)

        result = highlight(code, lexer, formatter)
        return result

    html_content = re.sub(
        code_block_pattern, replace_code_block, html_content, flags=re.DOTALL
    )
    return html_content


def markdown_to_html(input, output, template):
    with open(input, "r") as f:
        markdown_text = f.read()

    md = MarkdownIt("gfm-like").enable(["table"])
    html_body = md.render(markdown_text)

    html_body = apply_syntax_highlighting(html_body)

    with open(template, "r") as f:
        html_template = f.read()

    html_template = html_template.replace("<markdown-insert/>", html_body)

    pathlib.Path(output).parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w") as f:
        f.write(html_template)


def main():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )

    parser = argparse.ArgumentParser(
        prog="md2pdf",
        description="md2pdf turns markdown documents into pdfs with a custom template"
    )

    parser.add_argument(
        'input',
        type=pathlib.Path,
        default=pathlib.Path("index.md"),
        help="path to the input markdown file",
    )

    parser.add_argument(
        'output',
        type=pathlib.Path,
        nargs="?",
        default=pathlib.Path("out.pdf"),
        help="path to the output file (default: out.pdf)",
    )

    parser.add_argument(
        "-i",
        "--include",
        type=pathlib.Path,
        default=None,
        help="path of extra files to include in rendering (either directory or a single file) (default: None)",
    )

    parser.add_argument(
        "-t",
        "--template",
        type=pathlib.Path,
        default=pathlib.Path("./template/"),
        help="path to the template directory (default: ./template)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=False,
        help="more logging output"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        if args.include:
            temp_dir, addr = tempfileServer.start([args.include, args.template])
        else:
            temp_dir, addr = tempfileServer.start([args.template])

        markdown_to_html(
            input=args.input,
            output=temp_dir / "index.html",
            template=args.template / "index.html",
        )

        logging.debug('Temp Addr: ', addr)
    except FileNotFoundError as e: 
        logging.error("File '" + e.filename + "' does not exist.")
        quit()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto(addr, wait_until="networkidle")
        page.pdf(
            path=args.output,
            print_background=True
        )

        browser.close()

    if (args.verbose):
        input("Press enter to quit:")
