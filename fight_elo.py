from dataclasses import dataclass, field

@dataclass
class FightElo:
    k: float = 10.0
    beta: float = 200.0
    initial_rating: float = 1200.0
    points: dict = field(default_factory=dict, repr=False)
    fighters: dict = field(default_factory=dict, repr=False)
        
    def __post_init__(self):
        self.points = {
            'Draw': 0,
            'Decision-Split': 1,
            'Decision-Unanimous': 3,
            'Finish-Doctor': 4,
            'Finish-KO/TKO': 5,
            'Finish-Submission': 5
        }
        
    def add_fighter(self, name):
        '''
        Adds a fighter with the default ranking
        '''
        
        self.fighters[name] = self.initial_rating
        
    def __calc_probability(self, rating, rating_other):
        '''
        Calculates probability of winning based on ratings
        '''
        
        return 1 / (1 + (10 ** ((rating_other - rating) / (2 * self.beta))))
    
    def __calc_new_rating(self, rating, rating_other, win_by):
        '''
        Calculates new ratings based on two current ratings;
        Returns new ratings for both a loss and a win
        '''
        
        expected_score = self.__calc_probability(rating, rating_other)
        rating_if_loss = rating + self.k * self.points.get(win_by, 0) * (0 - expected_score)
        rating_if_win = rating + self.k * self.points.get(win_by, 0) * (1 - expected_score)
        return (rating_if_loss, rating_if_win)
    
    def update_ratings(self, fighter_winner, fighter_loser, win_by):
        '''
        Update figher ratings
        '''
        
        loss = 0
        win = 1
        
        if fighter_winner not in self.fighters.keys():
            self.add_fighter(fighter_winner)
            
        if fighter_loser not in self.fighters.keys():
            self.add_fighter(fighter_loser)
            
        rating_winner = self.fighters.get(fighter_winner)
        rating_loser = self.fighters.get(fighter_loser)
        
        new_ratings = self.__calc_new_rating(rating_winner, rating_loser, win_by)
        
        self.fighters[fighter_loser] = new_ratings[loss]
        self.fighters[fighter_winner] = new_ratings[win]
