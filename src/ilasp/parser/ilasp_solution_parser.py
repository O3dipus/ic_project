from gym_subgoal_automata.utils.subgoal_automaton import SubgoalAutomaton
from ilasp.ilasp_common import TRANSITION_STR, CONNECTED_STR, REJ_STR
from ilasp.parser.ilasp_parser_utils import parse_transition_rule, parse_edge_rule, parse_reject_rule

def parse_ilasp_solutions(ilasp_learnt_filename):
    rej_cond = ""
    with open(ilasp_learnt_filename) as f:
        automaton = SubgoalAutomaton()
        edges = {}
        for line in f:
            line = line.strip()
            if line.startswith(TRANSITION_STR):

                parsed_transition = parse_transition_rule(line)
                current_edge = (parsed_transition.src, parsed_transition.dst)
                if current_edge not in edges:
                    edges[current_edge] = []
                edges[current_edge].append(parsed_transition.body)

            elif line.startswith(CONNECTED_STR):
                parsed_edge = parse_edge_rule(line)
                current_edge = (parsed_edge.src, parsed_edge.dst)
                if current_edge not in edges:
                    edges[current_edge] = []
    
            elif line.startswith(REJ_STR): # rej_cond
                rej_cond = parse_reject_rule(line)

        if len(rej_cond) != 0:
            automaton.add_state("u_rej")
        for edge in edges:
            from_state, to_state = edge[0], edge[1]
            automaton.add_state(from_state)
            automaton.add_state(to_state)
            automaton.add_edge(from_state, to_state, edges[edge])
            if len(rej_cond) != 0:
                automaton.add_edge(from_state, "u_rej", [rej_cond])
        
        if len(rej_cond) != 0:
            automaton.add_edge("u_rej", "u_rej", [rej_cond])

        return automaton