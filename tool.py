from pypdf import PdfReader, PdfWriter

def extract_pages():
    reader = PdfReader("jpn_sched.pdf")

    pages = []
    for page in reader.pages:
        text = page.extract_text()

        nums = ""
        
        for char in text:
            if (not char.isnumeric()) and (char != '-') and (char != '&'):
                if len(nums) == 3 and '-' not in nums:
                    pages.append(nums)
                elif len(nums) == 7:
                    pages.append(nums)
                nums = ""
            else:
                nums += char


    page_nums = []
    for pg_nums in pages:
        if '-' in pg_nums:
            nums = pg_nums.split('-')
            start = int(nums[0])
            stop = int(nums[1]) + 1

            for page_num in range(start, stop):
                page_nums.append(int(page_num))
        elif '&' in pg_nums:
            nums = pg_nums.split('&')
            page_nums.append(int(nums[0]))
            page_nums.append(int(nums[1]))
        else:
            page_nums.append(int(pg_nums))

    return page_nums



def seperate_pages():
    writer = PdfWriter()
    reader = PdfReader("jpn_txtbk.pdf")
    page_nums = extract_pages()
    for pg_num in page_nums:
        writer.add_page(reader.pages[pg_num + 5])

    with open("jpn_hw.pdf", 'wb') as pdf:
        writer.write(pdf)


seperate_pages()

####################################################################################

def extract_pages_and_dates():
    reader = PdfReader("jpn_sched.pdf")

    pages = []
    for page in reader.pages:
        text = page.extract_text()

        nums = ""
        
        for char in text:
            if (char.isnumeric()) or (char == '-') or (char == '&') or (char == '/'):
                nums += char
            else:
                if len(nums) == 3 and '-' not in nums:
                    pages.append(nums)
                elif len(nums) == 7:
                    pages.append(nums)
                elif '/' in nums:
                    pages.append(nums)
                nums = ""
    return pages

def clean_pages_and_dates(pages_w_dates):
    hws = []
    pg_range = []
    for num in pages_w_dates:
        if '/' in num:
            if len(pg_range) > 1:
                hws.append(pg_range)
            pg_range = []
            pg_range.append(num)
        else:
            pg_range.append(num)

    return hws

def expand_page_ranges(condensed_hws):
    expanded_hws = []
    for hw in condensed_hws:
        pg_range = [hw[0]]
        for i in range(1, len(hw)):
            pg = hw[i]
            if '-' in pg:
                nums = pg.split('-')
                start = int(nums[0])
                stop = int(nums[1]) + 1

                for page_num in range(start, stop):
                    pg_range.append(int(page_num))
            elif '&' in pg:
                nums = pg.split('&')
                pg_range.append(int(nums[0]))
                pg_range.append(int(nums[1]))
            else:
                pg_range.append(int(pg))
        expanded_hws.append(pg_range)
    return expanded_hws

def get_hws_with_dates():
    pages_w_dates = extract_pages_and_dates()
    condensed_hws = clean_pages_and_dates(pages_w_dates)
    hws = expand_page_ranges(condensed_hws)
    return hws


def create_hws_with_dates():
    FOREWARD_OFFSET = 5
    hws = get_hws_with_dates()

    reader = PdfReader("jpn_txtbk.pdf")

    for hw in hws:
        writer = PdfWriter()
        for i in range(1, len(hw)):
            pg_num = hw[i] + FOREWARD_OFFSET
            writer.add_page(reader.pages[pg_num])
        due_date = hw[0]
        due_date = due_date.replace('/', '-') #mac doesnt allow / in filenames
        title = f"hws/jpn_hw_{due_date}.pdf"
        with open(title, "wb") as pdf:
            writer.write(pdf)


create_hws_with_dates()