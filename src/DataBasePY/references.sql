-- Create OHLCV indicators table query --
CREATE TABLE {PAIRNAME}_OHLCV_{candleSize.value}(timestamp TIMESTAMP PRIMARY KEY NOT NULL,
open DECIMAL({lowHigh}), high  DECIMAL({lowHigh}), low DECIMAL({lowHigh})
           close DECIMAL(), volume numeric(10), INDICATORS jsonb);


-- Create paper trader table query --
CREATE TABLE papertrader_results (
    session_id uuid PRIMARY KEY,
    running_on character varying, 
    session_start_time character varying,
    session_end_time character varying,
    strategy character varying,
    pair character varying,
    candle character varying,
    active boolean, 
    total_pnl numeric(5,3),
    principle numeric,
    transactions jsonb NOT NULL DEFAULT '[]'::jsonb
);

-- Create support/resistance table query -- 

CREATE TABLE support_resistance (

    pair character varying,
    candle character varying, 
    support numeric,
    resistance numeric,
    UNIQUE (pair, candle)
);