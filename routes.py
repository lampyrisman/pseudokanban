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
    "/post/step": {
        "target": "post_step"
    },
    "/post/step_del": {
        "target": "post_step_del"
    }
}

statics = {
    "/static/img": {
        "target": "get_images"
    },
    "/static/js": {
        "target": "get_js"
    }
}
