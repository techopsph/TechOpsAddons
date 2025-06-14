{
    "name": "Website Slides - Custom Video Embed",
    "version": "18.0",
    "summary": "Adds a custom embed code option to eLearning slides",
    "category": "Website/eLearning",
    "author": "Tech Ops PH",
    "website": "https://techops.ph",
    "depends": ["website_slides"],
    "data": [
        "views/slide_slide_views.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "website_slides_custom_video/static/src/js/slides_course_fullscreen_player.js",
            "website_slides_custom_video/static/src/xml/website_slides_fullscreen.xml",
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": False
}
