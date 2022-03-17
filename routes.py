routes = {
    "/": {
        "target": "get_main"
    },
    "/post/add": {
        "target": "post_task"
    },
    "/post/move":
        {
            "target": "post_move"
        },
}

statics = {
    "/static/img": {
        "target": "get_images"
    },
    "/static/js": {
        "target": "get_js"
    }
}
