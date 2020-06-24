import itertools
import operator


class CubeCasinoFormatter:
    def __init__(self, results):
        self.results = results

    def format(self):
        results_by_winner = itertools.groupby(self.results, operator.itemgetter(0))
        print(f"Results By Winner: {results_by_winner}")

        results = []
        for winner, winnings in results_by_winner:
            msg = f"@{winner} won "

            winnings_msg = " and ".join(
                [f"!{command} from @{loser}" for (_, loser, command) in winnings]
            )
            results.append(msg + winnings_msg)

        return results
