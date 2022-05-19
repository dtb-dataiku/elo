from dataclasses import dataclass, field

@dataclass
class ELO:
    k: float = 10.0
    beta: float = 200.0
    initial_rating: float = 1200.0
    points: dict = field(default_factory=dict, repr=False)
    competitors: dict = field(default_factory=dict, repr=False)
        
    def __post_init__(self):
        if len(self.points) == 0:
            self.points = {
                'Draw': 0,
                'Win': 1
            }
        
    def add_competitor(self, name):
        '''
        Adds a competitor with the default ranking
        '''
        
        self.competitors[name] = self.initial_rating
        
    def __calc_probability(self, rating, rating_other):
        '''
        Calculates probability of winning based on ratings
        '''
        
        return 1 / (1 + (10 ** ((rating_other - rating) / (2 * self.beta))))
    
    def __calc_new_rating(self, rating, rating_other, outcome):
        '''
        Calculates new ratings based on two current ratings;
        Returns new ratings for both a loss and a win
        '''
        
        expected_score = self.__calc_probability(rating, rating_other)
        rating_if_loss = rating + self.k * self.points.get(outcome, 0) * (0 - expected_score)
        rating_if_win = rating + self.k * self.points.get(outcome, 0) * (1 - expected_score)
        return (rating_if_loss, rating_if_win)
    
    def update_ratings(self, winner, loser, outcome):
        '''
        Update competitor ratings
        '''
        
        loss = 0
        win = 1
        
        if winner not in self.competitors.keys():
            self.add_competitor(winner)
            
        if loser not in self.competitors.keys():
            self.add_competitor(loser)
            
        rating_winner = self.competitors.get(winner)
        rating_loser = self.competitors.get(loser)
        
        new_ratings = self.__calc_new_rating(winner, loser, outcome)
        
        self.competitors[loser] = new_ratings[loss]
        self.competitors[winner] = new_ratings[win]
