class Partido:
    def __init__(self, equipo_home, equipo_away, fecha, estadio_id, estadio, id, lista_de_asientos, asistance, ventas, gastos_total):
        self.home_team = equipo_home
        self.away_team = equipo_away
        self.date = fecha
        self.stadium_id = estadio_id
        self.stadium = estadio
        self.id = id
        self.sits = lista_de_asientos
        self.asistance = asistance
        self.sell = ventas
        self.spends_total_vip = gastos_total