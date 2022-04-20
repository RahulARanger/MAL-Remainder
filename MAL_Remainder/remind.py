from flask import Flask, render_template
from MAL_Remainder.calendar_parse import previously
from MAL_Remainder.common_utils import open_local_url, close_main_thread_in_good_way, EnsurePort

app = Flask("remind")


@app.route('/')
def just_call():
    result = previously()

    if result < 0:
        close_main_thread_in_good_way()

    print(dir(result))
    return render_template(
        'remind.html'
    )


port = EnsurePort.get_free_port()
open_local_url(port)

app.run(port=port)
