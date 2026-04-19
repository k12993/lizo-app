from flask import Flask, render_template_string, request
from markupsafe import escape

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Lizo Back Office</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
        }

        .container {
            max-width: 500px;
            margin: auto;
            padding: 16px;
        }

        h1 {
            text-align: center;
            font-size: 20px;
        }

        label {
            font-size: 13px;
            font-weight: bold;
        }

        select, input {
            width: 100%;
            padding: 12px;
            margin-top: 6px;
            margin-bottom: 12px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 16px;
        }

        button {
            width: 100%;
            padding: 14px;
            background: black;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;
        }

        .mensaje {
            background: white;
            padding: 12px;
            border-radius: 10px;
            margin-top: 12px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        }

        textarea {
            width: 100%;
            border: none;
            resize: none;
            font-size: 14px;
            line-height: 1.4;
            outline: none;
        }

        .copy {
            margin-top: 8px;
            background: #28a745;
        }
    </style>
</head>

<body>

<div class="container">
    <h1>Lizo Back Office</h1>

    <form method="POST">
        <label>Modelo</label>
        <select name="modelo">
            <option {{ 'selected' if modelo == 'Core (Poliamida)' else '' }}>Core (Poliamida)</option>
            <option {{ 'selected' if modelo == 'Flex (Fibra de Bambú)' else '' }}>Flex (Fibra de Bambú)</option>
            <option {{ 'selected' if modelo == 'Modal (Premium)' else '' }}>Modal (Premium)</option>
        </select>

        <label>Nombre del Cliente</label>
        <input type="text" name="cliente" value="{{ cliente or '' }}" required>

        <label>Tipo</label>
        <select name="tipo">
            <option {{ 'selected' if tipo == 'Primer Contacto' else '' }}>Primer Contacto</option>
            <option {{ 'selected' if tipo == 'Desarrollo' else '' }}>Desarrollo</option>
            <option {{ 'selected' if tipo == 'Post Venta' else '' }}>Post Venta</option>
        </select>

        <button type="submit">Generar Mensajes</button>
    </form>

    {% if mensajes %}
        <h2 style="font-size:16px;margin-top:16px;">Mensajes</h2>

        {% for mensaje in mensajes %}
            <div class="mensaje">
                <textarea id="msg{{ loop.index }}" rows="4">{{ mensaje }}</textarea>
                <button class="copy" onclick="copiar('msg{{ loop.index }}')">Copiar</button>
            </div>
        {% endfor %}
    {% endif %}
</div>

<script>
function copiar(id) {
    const el = document.getElementById(id);

    if (navigator.clipboard) {
        navigator.clipboard.writeText(el.value)
        .then(() => alert("Copiado"))
        .catch(() => fallbackCopy(el));
    } else {
        fallbackCopy(el);
    }
}

function fallbackCopy(el) {
    el.select();
    el.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Copiado");
}
</script>

</body>
</html>
"""

def generar_mensajes(cliente, modelo, tipo):
    cliente = escape(cliente)
    saludo = f"Hola {cliente},"

    # ================= CORE =================
    if "Core" in modelo:

        if tipo == "Primer Contacto":
            return [
                f"{saludo} te cuento: el modelo Core está hecho de poliamida y elastano, lo que hace que sea mucho más fresco y ligero que el algodón. La mayoría de clientes lo elige porque elimina ese calor incómodo del día a día y además tiene una pretina ultradelgada que no aprieta. Tenemos pack de 3 por S/60. ¿Buscas más frescura o comodidad principalmente?",
                f"{cliente}, si lo que te incomoda es el calor o la falta de ventilación, el Core es justo para eso. Es más fresco que el algodón, más ligero y no genera presión en la cintura. Pack de 3 por S/60. ¿Te gustaría probarlo?",
                f"{saludo} el Core está pensado para quienes quieren dar el salto a algo más cómodo y fresco en su día a día. Se siente diferente desde el primer uso: más ligero, más transpirable y sin esa incomodidad típica. Pack de 3 por S/60."
            ]

        elif tipo == "Desarrollo":
            return [
                f"{saludo} buenísima elección el Core. Para recomendarte bien la talla, ¿qué talla sueles usar? Si tienes dudas, dime tu estatura y peso. 👉 ¿Has tenido cambios físicos en los últimos 3 meses?",
                f"{cliente}, el Core funciona mejor con la talla correcta. Dime qué talla usas o pásame tu estatura y peso y te asesoro mejor. ¿Has tenido cambios recientes en tu físico?",
                f"{saludo} para aprovechar el Core al máximo, es clave elegir bien la talla. Cuéntame tu talla o tu estatura y peso. 👉 ¿Has subido o bajado de peso recientemente?"
            ]

        else:
            return [
                f"{saludo} ¿cómo te fue con el modelo Core? 👉 ¿Sentiste la diferencia en frescura y comodidad durante el día?",
                f"{cliente}, cuéntame qué tal te resultó el Core. 👉 ¿Lo sentiste más ligero que lo que usabas antes?",
                f"{saludo} estamos haciendo seguimiento. 👉 ¿Cómo te sentiste en frescura y comodidad? Si te gustó, luego puedes armar packs."
            ]

    # ================= FLEX =================
    elif "Flex" in modelo:

        if tipo == "Primer Contacto":
            return [
                f"{saludo} el modelo Flex está hecho de fibra de bambú, lo que lo hace naturalmente fresco, antibacteriano y ideal si buscas evitar olores o irritaciones. Es perfecto para piel sensible. Tenemos pack de 4 por S/80. ¿Buscas algo más natural o comodidad diaria?",
                f"{cliente}, si alguna vez has tenido incomodidad, sudor o irritación, el Flex te va a funcionar mejor. La fibra de bambú es más suave, respira mejor y mantiene frescura todo el día. Pack de 4 por S/80.",
                f"{saludo} muchos clientes eligen el Flex porque es más suave, más fresco y cuida mejor la piel. Es una opción más saludable frente a lo tradicional. Pack de 4 por S/80."
            ]

        elif tipo == "Desarrollo":
            return [
                f"{saludo} el Flex es ideal para comodidad y suavidad. ¿Qué talla usas? Si tienes dudas, dime tu estatura y peso. 👉 ¿Has tenido cambios físicos recientes?",
                f"{cliente}, el Flex se adapta bien, pero la talla correcta hace la diferencia. ¿Usas M o L? Si no estás seguro, dime tu estatura y peso. ¿Has tenido cambios en tu físico?",
                f"{saludo} para que el Flex te quede perfecto, cuéntame tu talla o tu estatura y peso. 👉 ¿Has tenido cambios en los últimos 3 meses?"
            ]

        else:
            return [
                f"{saludo} ¿cómo te fue con el modelo Flex? 👉 ¿Sentiste la frescura natural durante el día?",
                f"{cliente}, cuéntame tu experiencia. 👉 ¿Te resultó cómodo y sin irritaciones?",
                f"{saludo} estamos haciendo seguimiento. 👉 ¿Notaste diferencia en suavidad, frescura o control de olores?"
            ]

    # ================= MODAL =================
    elif "Modal" in modelo:

        if tipo == "Primer Contacto":
            return [
                f"{saludo} el modelo Modal está hecho de fibras de origen natural que logran una tela mucho más suave, ligera y fresca. Es la opción más premium si buscas comodidad superior en el día a día. ¿Buscas algo más cómodo o más duradero?",
                f"{cliente}, el Modal es otro nivel en comodidad. Es extremadamente suave, se adapta perfecto al cuerpo y se siente ligero todo el día. Es ideal si quieres algo superior a lo tradicional.",
                f"{saludo} si lo que buscas es lo mejor en comodidad, el Modal es la mejor opción. Más suave, más fresco y más cómodo desde el primer uso."
            ]

        elif tipo == "Desarrollo":
            return [
                f"{saludo} el Modal se siente mejor con la talla exacta. ¿Qué talla usas? Si tienes dudas, dime tu estatura y peso. 👉 ¿Has tenido cambios físicos recientes?",
                f"{cliente}, para que el Modal se sienta realmente cómodo, es clave elegir la talla correcta. ¿Usas M o L? Si no estás seguro, pásame tu estatura y peso. ¿Has tenido cambios en tu físico?",
                f"{saludo} el Modal depende mucho de la talla correcta. Cuéntame tu talla o tu estatura y peso. 👉 ¿Has subido o bajado de peso recientemente?"
            ]

        else:
            return [
                f"{saludo} ¿cómo te fue con el Modal? 👉 ¿Sentiste la suavidad desde el primer uso?",
                f"{cliente}, cuéntame tu experiencia. 👉 ¿Te resultó más cómodo que lo anterior?",
                f"{saludo} estamos haciendo seguimiento. 👉 ¿Cumplió con lo que esperabas en confort?"
            ]

    return []


@app.route("/", methods=["GET", "POST"])
def home():
    mensajes = []
    cliente = ""
    modelo = ""
    tipo = ""

    if request.method == "POST":
        modelo = request.form["modelo"]
        cliente = request.form["cliente"]
        tipo = request.form["tipo"]

        mensajes = generar_mensajes(cliente, modelo, tipo)

    return render_template_string(
        HTML,
        mensajes=mensajes,
        cliente=cliente,
        modelo=modelo,
        tipo=tipo
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
