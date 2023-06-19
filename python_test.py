bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png">
    </div>
    <div class="message">
        {% if "no relevant data" in MSG or if "sorry" in MSG%}
            sorry could not find any data on that 
        {% else %}
            {{ MSG }}
        {% endif %}
    </div>
</div>
'''