from data import build_nodes_demo, build_court_record_demo
from scriptIMAC import nodes, court_record
from game import Game

if __name__ == "__main__":

    # Script original du jeu
    # nodes = build_nodes_demo()
    # court_record = build_court_record_demo()
    # Game(nodes, starting_node_id="q1_date", lifes=5.0, courtRecord=court_record).run()

    # Script IMAC
    nodes = nodes()
    court_record = court_record()
    Game(nodes, starting_node_id="s1-date", lifes=5.0, courtRecord=court_record).run()
