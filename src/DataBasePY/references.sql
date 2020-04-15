-- Create table query --
CREATE TABLE {PAIRNAME}_OHLCV_{candleSize.value}(timestamp TIMESTAMP PRIMARY KEY NOT NULL,
open DECIMAL({lowHigh}), high  DECIMAL({lowHigh}), low DECIMAL({lowHigh})
           close DECIMAL(), volume numeric(10), INDICATORS jsonb);