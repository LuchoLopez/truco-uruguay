import cherrypy
import jsonpickle
import json
import Tests
import logging


DEBUG = False
LEVEL = logging.INFO
logger = logging.getLogger('truco')
logger.setLevel(logging.DEBUG if DEBUG else LEVEL)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG if DEBUG else LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Root(object):
    @cherrypy.expose
    def index(self):
        return """
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        </head>
        <body>
            <button onclick="repartir()" style="margin-bottom: 50px;">Repartir</button>
            <div id="mesa">
            </div>
            <script type="text/javascript">
            function repartir() {
                $('#mesa').empty();
                $.getJSON('/ws/test').done( function(data){
                        $( "<div>" ).attr("id", "muestra").attr("style", "float:left").appendTo("#mesa");
                        var mpalo = data['j1'].muestra.palo;
                        var mnumero = data['j1'].muestra.numero_mostrar;
                        $( "<h3>" ).text("muestra").appendTo("#muestra");
                        $( "<img>" ).attr( "src", "/static/cartas/" + mpalo + "/" + mnumero + ".jpg" ).appendTo( "#muestra" );

                        $.each(data, function(jugador){ 
                            $( "<div>" ).attr("id", jugador).attr("style", "float:left;").appendTo("#mesa");
                            $( "<h3>" ).text(jugador).appendTo("#" + jugador);
                            
                            $.each(data[jugador].cartas, function(carta){
                                var palo = data[jugador].cartas[carta].palo;
                                var numero = data[jugador].cartas[carta].numero_mostrar;
                                $( "<img>" ).attr( "src", "/static/cartas/" + palo + "/" + numero + ".jpg" ).appendTo( "#" + jugador );
                            });
                            
                            $( "<p>" ).text("Flor: " + data[jugador].es_flor).appendTo("#" + jugador);
                            $( "<p>" ).text("Puntos: " + data[jugador].puntos).appendTo("#" + jugador);
                        });
                    });
            };
            </script>
        </body>
        </html>
        """


class WS(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test(self):
        r = jsonpickle.encode(Tests.testear(), unpicklable=False)
        return json.loads(r)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def debug(self):
        r = jsonpickle.encode(Tests.test_puntuacion(), unpicklable=False)
        return json.loads(r)


if __name__ == '__main__':
    cherrypy.config.update("server.conf")
    cherrypy.tree.mount(Root(), "/", "app.conf")
    cherrypy.tree.mount(WS(), "/ws")
    cherrypy.engine.start()
    cherrypy.engine.block()

