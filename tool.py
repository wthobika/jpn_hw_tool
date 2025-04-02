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