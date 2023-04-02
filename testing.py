"""Main module to test each sample against each API"""
import time
import pandas as pd # pylint: disable=import-error
import test_hear as th

def flatten(list_of_lists):
    """Flatten a list of lists"""
    return [item for sublist in list_of_lists for item in sublist]

def main():
    """Test each sample against each API"""
    start_time = time.time()
    # create a dictionary of sample names and their file paths
    # transcriptions may not include punctuation, accents, etc, but these get stripped anyway
    file_info = {
        "¿Cómo te llamas?": "samples/easy/comotellamas.wav",
        "¿Cómo estás?": "samples/easy/comoestas.wav",
        "A dónde vas": "samples/easy/adondevas.wav",
        "Alto": "samples/easy/alto.wav",
        "¿A qué hora es?": "samples/easy/aquehoraes.wav",
        "Bien hecho": "samples/easy/bienhecho.wav",
        "Bienvenido": "samples/easy/bienvenido.wav",
        "Buena onda": "samples/easy/buenaonda.wav",
        "Buenas noches": "samples/easy/buenasnoches.wav",
        "Buena suerte": "samples/easy/buenasuerte.wav",
        "Buen provecho": "samples/easy/buenprovecho.wav",
        "Comiendo moscas": "samples/easy/comiendomoscas.wav",
        "¿Cuál es tu cancion favorita?": "samples/easy/cualestucancionfavorita.wav",
        "¿Cuál es tu libro favorito?": "samples/easy/cualestulibrofavorito.wav",
        "¿Cuál es tu pelicula favorita?": "samples/easy/cualestupeliculafavorita.wav",
        "¿De donde eres?": "samples/easy/dedondeeres.wav",
        "De nada": "samples/easy/denada.wav",
        "Disculpa": "samples/easy/disculpa.wav",
        "¿Dónde está el baño?": "samples/easy/dondeestaelbano.wav",
        "¿Dónde vives?": "samples/easy/dondevives.wav",
        "¿En qué te trabajas?": "samples/easy/enquetetrabajas.wav",
        "¿Es esto correcto?": "samples/easy/esestocorrecto.wav",
        "¿Estas lista?": "samples/easy/estaslista.wav",
        "¿Estas listo?": "samples/easy/estaslisto.wav",
        "¿Estoy perdido?": "samples/easy/estoyperdido.wav",
        "Felicitaciones": "samples/easy/felicitaciones.wav",
        "Feliz cumpleaños": "samples/easy/felizcumpleanos.wav",
        "Genial": "samples/easy/genial.wav",
        "Gracias": "samples/easy/gracias.wav",
        "Hasta pronto": "samples/easy/hastapronto.wav",
        "Hola": "samples/easy/hola.wav",
        "Increíble": "samples/easy/increible.wav",
        "Lo siento": "samples/easy/losiento.wav",
        "Mala leche": "samples/easy/malaleche.wav",
        "Me encanta el café": "samples/easy/meencantaelcafe.wav",
        "Me gusta ir al museo": "samples/easy/megustairalmuseo.wav",
        "Me llamo Dani": "samples/easy/mellamodani.wav",
        "Mucho gusto": "samples/easy/muchogusto.wav",
        "No entiendo": "samples/easy/noentiendo.wav",
        "No hablo español": "samples/easy/nohabloespanol.wav",
        "No me interesa": "samples/easy/nomeinteresa.wav",
        "No sé": "samples/easy/nose.wav",
        "Nos vemos": "samples/easy/nosvemos.wav",
        "No tan bien": "samples/easy/notanbien.wav",
        "Papando moscas": "samples/easy/papandomoscas.wav",
        "Pasa algo": "samples/easy/pasaalgo.wav",
        "Perdon": "samples/easy/perdon.wav",
        "Ponte las pilas": "samples/easy/pontelaspilas.wav",
        "Puedo entrar": "samples/easy/puedoentrar.wav",
        "¿Qué es esto?": "samples/easy/queesesto.wav",
        "¿Qué haces ahora?": "samples/easy/quehacesahora.wav",
        "¿Qué hora es?": "samples/easy/quehoraes.wav",
        "¿Qué musica te gusta?": "samples/easy/quemusicategusta.wav",
        "¿Qué significa eso?": "samples/easy/quesignificaeso.wav",
        "¿Qué tal?": "samples/easy/quetal.wav",
        "¿Qué te gusta leer?": "samples/easy/quetegustaleer.wav",
        "¿Quieres tomar una copa?": "samples/easy/quierestomarunacopa.wav",
        "¿Sabes que pasa?": "samples/easy/sabesquepasa.wav",
        "Salud": "samples/easy/salud.wav",
        "Soy de estados unidos": "samples/easy/soydeestadosunidos.wav",
        "¿Te gusta tu trabajo?": "samples/easy/tegustatutrabajo.wav",
        "Trabajo en una escuela": "samples/easy/trabajoenunaescuela.wav",
        "Vivo en california": "samples/easy/vivoencalifornia.wav",
        "¿Y tú?": "samples/easy/ytu.wav"
    }


    # iterate through the dictionary and test each sample
    results = [th.test_options(file, phrase) for phrase, file in file_info.items()]
    flat_results = flatten(results)
    col_names = ["Text", "API", "Time", "WER", "MER", "WIL"]
    results_df = pd.DataFrame(flat_results, columns=col_names)
    results_df.to_csv("raw_results.csv", index=False)
    total_time = time.time() - start_time
    print(total_time)

if __name__ == "__main__":
    main()
