from .schemas import Blog

def paginateDashboard(page:int,limit:int,docs:list[Blog]):
    page_index = (page-1)*limit
    return docs[page_index:(page_index+limit)]