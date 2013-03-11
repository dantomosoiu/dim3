def page_url( request ):
    return { 'pageurl': request.get_full_path() }