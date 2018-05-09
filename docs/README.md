# Precision Informatics engine (PIe)
Python wrapper for tools with corresponding CWL

{% for collection in site.collections %}
<h1>{{ collection[0] }} has the following document:</h1>
    {% for document in collection[1].docs %}
        <p><a href="{{ document.relative_path }}">{{ document.title }}</a></p>
    {% endfor %}
{% endfor %}
