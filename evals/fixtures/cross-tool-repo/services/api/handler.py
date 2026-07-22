def handle(request):
    verify_signature(request.body, request.signature)
    return parse_json(request.body)
