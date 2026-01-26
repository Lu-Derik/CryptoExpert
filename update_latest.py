import os
import datetime
import re

def get_sorted_dates():
    content_dir = 'content'
    dates = []
    if not os.path.exists(content_dir):
        return dates

    for year in os.listdir(content_dir):
        if not year.isdigit(): continue
        year_path = os.path.join(content_dir, year)
        
        for month in os.listdir(year_path):
            if not month.isdigit(): continue
            month_path = os.path.join(year_path, month)
            
            for day in os.listdir(month_path):
                if not day.isdigit(): continue
                # check if index.html exists
                if os.path.exists(os.path.join(month_path, day, 'index.html')):
                    dates.append(datetime.date(int(year), int(month), int(day)))
    
    dates.sort(reverse=True)
    return dates

def generate_sidebar_html(dates):
    if not dates:
        return ""
    
    latest_date = dates[0]
    history_html = ""
    
    # Group by Year -> Month
    tree = {}
    for d in dates:
        if d.year not in tree: tree[d.year] = {}
        if d.month not in tree[d.year]: tree[d.year][d.month] = []
        tree[d.year][d.month].append(d)

    for year in sorted(tree.keys(), reverse=True):
        history_html += f"""
                        <details class="group" open>
                            <summary class="flex items-center cursor-pointer list-none text-sm font-medium text-gray-600 dark:text-gray-300">
                                <i class="fa-solid fa-chevron-right mr-2 text-[10px] transition-transform group-open:rotate-90"></i>
                                {year}
                            </summary>
                            <ul class="ml-6 mt-2 space-y-2 border-l border-gray-200 dark:border-gray-800">"""
        
        for month in sorted(tree[year].keys(), reverse=True):
            month_name = datetime.date(year, month, 1).strftime("%B")
            history_html += f"""
                                <li>
                                    <details class="group/month">
                                        <summary class="flex items-center cursor-pointer list-none text-sm font-medium text-gray-500 py-1 pl-4 hover:text-apple-blue">
                                            {month_name}
                                        </summary>
                                        <ul class="ml-4 mt-1 space-y-1">"""
            
            for d in tree[year][month]:
                link = f"/content/{d.year}/{d.month:02d}/{d.day:02d}/"
                history_html += f"""
                                            <li><a href="{link}" class="text-xs text-gray-400 hover:text-apple-blue pl-4 py-1 block">{d.day}th Insight</a></li>"""
            
            history_html += """
                                        </ul>
                                    </details>
                                </li>"""
        
        history_html += """
                            </ul>
                        </details>"""
    
    return history_html

def update_index_html():
    dates = get_sorted_dates()
    if not dates:
        print("No content found.")
        return

    latest_date = dates[0]
    latest_link = f"/content/{latest_date.year}/{latest_date.month:02d}/{latest_date.day:02d}/"
    latest_date_str = latest_date.strftime("%Y-%m-%d")

    sidebar_content = generate_sidebar_html(dates)

    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update Latest Link and Date
        # Find the <a> tag within the "Latest" section
        latest_section_pattern = r'(<div>\s*<h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Latest</h3>\s*<ul class="space-y-2">\s*<li>\s*)<a href="[^"]+" class="flex items-center p-3 rounded-xl bg-apple-blue text-white shadow-lg shadow-blue-500/30">\s*<span class="text-sm font-medium">[^<]+</span>'
        
        latest_replacement = f'\\1<a href="{latest_link}" class="flex items-center p-3 rounded-xl bg-apple-blue text-white shadow-lg shadow-blue-500/30">\\n                                <span class="text-sm font-medium">{latest_date_str}</span>'
        
        if re.search(latest_section_pattern, content):
            content = re.sub(latest_section_pattern, latest_replacement, content)
        else:
            print("Warning: Could not find 'Latest' section in index.html")

        # Update History Section
        history_section_pattern = r'(<div id="history-nav">\s*<h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">History</h3>\s*<div class="space-y-4">)([\s\S]*?)(</div>\s*</div>)'
        
        if re.search(history_section_pattern, content):
            content = re.sub(history_section_pattern, f'\\1{sidebar_content}\\3', content)
        else:
            print("Warning: Could not find 'History' section in index.html")
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Successfully updated index.html with latest date: {latest_date_str}")

    except FileNotFoundError:
        print("index.html not found.")

if __name__ == "__main__":
    update_index_html()
