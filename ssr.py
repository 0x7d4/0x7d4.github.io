# site_generator.py
import os
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

# https://stackoverflow.com/a/182259/12696223
class Monkey(object):
    def __init__(self, path: str, fn : callable):
        self._cached_stamp = 0
        self.filename = path
        self.fn = fn

    def watch(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            print("File changed")
            self._cached_stamp = stamp
            self.fn()
            
	def check_multi_files(self, files: list):
        

    def start(self, interval : float =1.0):
        while True:
            self.watch()
            time.sleep(interval)


def generate_site(template_file, articles_dir, build_dir):
    # Read the template content from the file
    with open(template_file, "r") as template:
        template_content = template.read()

    # Create the build directory if it doesn't exist
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    # Iterate over HTML articles in the articles directory
    for article_filename in os.listdir(articles_dir):
        if article_filename.endswith(".html"):
            # Read the content of the article
            with open(
                os.path.join(articles_dir, article_filename), "r"
            ) as article_file:
                article_content = article_file.read()

            # Get the article title from the filename
            article_title = os.path.splitext(article_filename)[0]

            # Replace <view></view> with article content in the template
            page_content = template_content.replace(
                "<view></view>",
                f"<article><h1>{article_title}</h1>\n{article_content}</article>",
            )

            # Create the output filename based on the article title
            output_filename = os.path.join(
                build_dir, f"{article_title.lower().replace(' ', '-')}.html"
            )

            # Write the page content to the output HTML file
            with open(output_filename, "w") as output_file:
                output_file.write(page_content)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Generate a static site.")

    parser.add_argument("template", help="The template file path (e.g. template.html)")
    parser.add_argument("articles", help="The articles directory path (e.g. articles)")
    parser.add_argument(
        "-o", "--output", help="The build directory path (e.g. build)", default="build"
    )
    # watch option
    parser.add_argument("-w", "--watch", help="Watch for changes", action="store_true")

    # Generate the static site
    args = parser.parse_args()

    # print "Generating site..." in blue
    print("\033[94m" + "Generating site..." + "\033[0m")
    generate_site(args.template, args.articles, args.output)
    # print "Site is ready in " + args.output + " directory" in green
    print("\033[92m" + "Site is ready in /" + args.output + "\033[0m")
    if args.watch:
        monkey = Monkey(args.articles + "/article_1.html", lambda: generate_site(args.template, args.articles, args.output))
        monkey.start()

