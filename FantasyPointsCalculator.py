import pandas as pd
def ScoreCalc(runs,FBalls,Fours,Sixes,dismissals,wickets,overs,Catches,Stumping,Maidens,StrikeRate,Economy,RunOut):
    score=0
    
    score+=runs
    score+=Fours*1
    score+=Sixes*2
    if runs>=50:
        score+=4
    if runs>=100:
        score+=8
    if dismissals==0 and runs==0:
        score-=3
    
    if FBalls>=10:
        sr=StrikeRate
        if 50<=sr<=60:
            score-=4
        elif 60<=sr<70:
            score-=2
        elif sr<50:
            score-=6
    
    score+=wickets*25
    if wickets>=3:
        score+=4
    if wickets>=4:
        score+=8
    if wickets>=5:
        score+=16

    score+=Maidens*4
    
    if overs>=2:
        er=Economy
        if er<5:
            score+=6
        elif 5<=er<6:
            score+=4
        elif 6<=er<7:
            score+=2
        elif er>10:
            score-=6
    
    score+=Catches*8
    if Catches>=3:
        score+=4
    score+=Stumping*12
    score+=RunOut*8
    
    return score


df=pd.read_csv('WholeData.csv')
df['Score']=df.apply(
    lambda x: ScoreCalc(
        x['Runs'],
        x['FBalls'],
        x['Fours'],
        x['Sixes'],
        x['Dismissals'],
        x['Wickets'],
        x['Overs'],
        x['Catches'],
        x['Stumpings'],
        x['Maidens'],
        x['StrikeRate'],
        x['Economy'],
        x['RunOuts']
        ),axis=1)        
        
df.to_csv('DataWithScore.csv',index=False)