"""
Quant Challenge 2025

Algorithmic strategy template
"""

from enum import Enum
from typing import Optional
import math

class Side(Enum):
    BUY = 0
    SELL = 1

class Ticker(Enum):
    # TEAM_A (home team)
    TEAM_A = 0

def place_market_order(side: Side, ticker: Ticker, quantity: float) -> None:
    """Place a market order.
    
    Parameters
    ----------
    side
        Side of order to place
    ticker
        Ticker of order to place
    quantity
        Quantity of order to place
    """
    return

def place_limit_order(side: Side, ticker: Ticker, quantity: float, price: float, ioc: bool = False) -> int:
    """Place a limit order.
    
    Parameters
    ----------
    side
        Side of order to place
    ticker
        Ticker of order to place
    quantity
        Quantity of order to place
    price
        Price of order to place
    ioc
        Immediate or cancel flag (FOK)

    Returns
    -------
    order_id
        Order ID of order placed
    """
    return 0

def cancel_order(ticker: Ticker, order_id: int) -> bool:
    """Cancel an order.
    
    Parameters
    ----------
    ticker
        Ticker of order to cancel
    order_id
        Order ID of order to cancel

    Returns
    -------
    success
        True if order was cancelled, False otherwise
    """
    return 0

class Strategy:
    """Template for a strategy."""

    def reset_state(self) -> None:
        """Reset the state of the strategy to the start of game position.
        
        Since the sandbox execution can start mid-game, we recommend creating a
        function which can be called from __init__ and on_game_event_update (END_GAME).

        Note: In production execution, the game will start from the beginning
        and will not be replayed.
        """
        self.position: int = 0
        self.entry_price: Optional[float] = None
        self.capital: float = 100000.0
        self.quantity: float = 100.0
        self.home_score: int = 0
        self.away_score: int = 0
        self.time_seconds: float = 48 * 60  # assume basketball 48 minutes

    def __init__(self) -> None:
        """Your initialization code goes here."""
        self.reset_state()

    def model_probability(self) -> float:
        """Logistic win probability model using score differential and time."""
        score_diff = self.home_score - self.away_score
        time_frac = max(self.time_seconds, 1) / (48 * 60)  # normalize to [0,1]
        k = 0.1  # aggressiveness parameter
        return 1 / (1 + math.exp(-k * score_diff / time_frac))
    def on_orderbook_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        market_prob = price / 100.0
        model_prob = self.model_probability()

        # Buy if undervalued
        if self.position == 0 and market_prob < model_prob * 0.90:
            print(f"BUY: Market {market_prob:.2f}, Model {model_prob:.2f}")
            place_market_order(Side.BUY, ticker, self.quantity)
            self.position = 1
            self.entry_price = market_prob

        # Sell if overvalued
        elif self.position == 1 and market_prob > model_prob * 1.05:
            print(f"SELL: Market {market_prob:.2f}, Model {model_prob:.2f}")
            place_market_order(Side.SELL, ticker, self.quantity)
            self.position = 0
            self.entry_price = None

    def on_trade_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        print(f"Trade update: {ticker} {side} {quantity} @ {price}")

    def on_account_update(self, ticker: Ticker, side: Side, price: float, quantity: float, capital_remaining: float) -> None:
        self.capital = capital_remaining
        print(f"Account update: {side} {quantity} @ {price}, capital {capital_remaining}")

    def on_game_event_update(self,
                           event_type: str,
                           home_away: str,
                           home_score: int,
                           away_score: int,
                           player_name: Optional[str],
                           substituted_player_name: Optional[str],
                           shot_type: Optional[str],
                           assist_player: Optional[str],
                           rebound_type: Optional[str],
                           coordinate_x: Optional[float],
                           coordinate_y: Optional[float],
                           time_seconds: Optional[float]
        ) -> None:

        self.home_score = home_score
        self.away_score = away_score
        if time_seconds is not None:
            self.time_seconds = time_seconds

        print(f"Event {event_type}: Score {home_score}-{away_score}, Time {self.time_seconds}s")

        if event_type == "END_GAME":
            self.reset_state()
    
    # def on_trade_update(
    #     self, ticker: Ticker, side: Side, quantity: float, price: float
    # ) -> None:
    #     """Called whenever two orders match. Could be one of your orders, or two other people's orders.
    #     Parameters
    #     ----------
    #     ticker
    #         Ticker of orders that were matched
    #     side:
    #         Side of orders that were matched
    #     quantity
    #         Volume traded
    #     price
    #         Price that trade was executed at
    #     """
    #     print(f"Python Trade update: {ticker} {side} {quantity} shares @ {price}")

    # def on_orderbook_update(
    #     self, ticker: Ticker, side: Side, quantity: float, price: float
    # ) -> None:
    #     """Called whenever the orderbook changes. This could be because of a trade, or because of a new order, or both.
    #     Parameters
    #     ----------
    #     ticker
    #         Ticker that has an orderbook update
    #     side
    #         Which orderbook was updated
    #     price
    #         Price of orderbook that has an update
    #     quantity
    #         Volume placed into orderbook
    #     """
    #     pass

    # def on_account_update(
    #     self,
    #     ticker: Ticker,
    #     side: Side,
    #     price: float,
    #     quantity: float,
    #     capital_remaining: float,
    # ) -> None:
    #     """Called whenever one of your orders is filled.
    #     Parameters
    #     ----------
    #     ticker
    #         Ticker of order that was fulfilled
    #     side
    #         Side of order that was fulfilled
    #     price
    #         Price that order was fulfilled at
    #     quantity
    #         Volume of order that was fulfilled
    #     capital_remaining
    #         Amount of capital after fulfilling order
    #     """
    #     pass

    # def on_game_event_update(self,
    #                        event_type: str,
    #                        home_away: str,
    #                        home_score: int,
    #                        away_score: int,
    #                        player_name: Optional[str],
    #                        substituted_player_name: Optional[str],
    #                        shot_type: Optional[str],
    #                        assist_player: Optional[str],
    #                        rebound_type: Optional[str],
    #                        coordinate_x: Optional[float],
    #                        coordinate_y: Optional[float],
    #                        time_seconds: Optional[float]
    #     ) -> None:
    #     """Called whenever a basketball game event occurs.
    #     Parameters
    #     ----------
    #     event_type
    #         Type of event that occurred
    #     home_score
    #         Home team score after event
    #     away_score
    #         Away team score after event
    #     player_name (Optional)
    #         Player involved in event
    #     substituted_player_name (Optional)
    #         Player being substituted out
    #     shot_type (Optional)
    #         Type of shot
    #     assist_player (Optional)
    #         Player who made the assist
    #     rebound_type (Optional)
    #         Type of rebound
    #     coordinate_x (Optional)
    #         X coordinate of shot location in feet
    #     coordinate_y (Optional)
    #         Y coordinate of shot location in feet
    #     time_seconds (Optional)
    #         Game time remaining in seconds
    #     """

    #     print(f"{event_type} {home_score} - {away_score}")

    #     if event_type == "END_GAME":
    #         # IMPORTANT: Highly recommended to call reset_state() when the
    #         # game ends. See reset_state() for more details.
    #         self.reset_state()
    #         return
