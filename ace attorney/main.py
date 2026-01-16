from data import build_nodes_demo, build_court_record_demo
from game import Game

if __name__ == "__main__":
    nodes = build_nodes_demo()
    court_record = build_court_record_demo()
    Game(nodes, starting_node_id="q1_date", lifes=5.0, courtRecord=court_record).run()
