import React, { useRef } from 'react'
import { makeStyles } from '@material-ui/core';
import { useState } from 'react'
import background from './images/backgroundResult.png';
import Bar from './Bar';
import Chart from './Chart';
import { Link } from 'react-router-dom'

const useStyle = makeStyles({
    container: {
        marginTop : "3rem",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center"
    },
    scoreContainer: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center"

    },
    background: {
        backgroundImage: `url(${background})`,
        backgroundSize: 'cover',
        // height: '100vh',
        width: '100vw',
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: "flex-start",
        fontFamily: 'Raleway',
        zIndex: "-1",
    },
    finalScore: {
        fontSize: "2rem",
        fontWeight: "bold",
        color: "#FFA114",
    },
    score: {
        fontSize: "4rem",
        fontWeight: "bold",
        marginBottom: "1rem"
    },
    mainMenu: {
        width: "13rem",
        height: "4rem",
        marginTop : "1rem",
        background: "linear-gradient(#FFC267, #FFBD5A)",
        border: "none",
        fontSize: "1.25rem",
        borderRadius: ".5rem",
        fontFamily: "Raleway",
        fontWeight: "bold",
        color: "#FFFFFF",
    },
    chart: {
        marginTop: "3rem",
        marginBottom: "2rem",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center"
    },
    chartTitle: {
        fontSize: "1.5rem",
        fontWeight: "bold",
        marginBottom: "1rem"
    }
})

export const Result = ({numbers,interval,average,video}) => {
    const classes = useStyle()
    const score = average
    const displayedScore = Math.floor(score * 100)
    const videoRef = useRef(null)
    let props = { score }

    function handleClick(x,y){
        if (isFinite(x)){
            debugger
            videoRef.current.currentTime = x 

        }

    }

    return (
        <>
            <div className={classes.background}>
                <div className={classes.container}>
                    <div className={classes.scoreContainer}>
                        <div className={classes.finalScore}>
                            FINAL SCORE
                        </div>
                        <div className={classes.score}>
                            {displayedScore}%
                        </div>
                        <div>
                            <Bar {...props}></Bar>
                        </div>
                    </div>
                    <div className={classes.chart}>
                        <div className={classes.chartTitle}>
                            Attention Span over Time
                        </div>
                        <Chart numbers={numbers} interval={interval} handleClick={handleClick}></Chart>
                    </div>
                    <video width="400" controls ref={videoRef}>
                        <source src={URL.createObjectURL(video)}></source>
                    </video>
                    <Link to="/" exact="true">
                    <div>
                        <input type="button" className={classes.mainMenu} value="MAIN MENU"></input>
                    </div>
                    </Link>
                </div>
            </div>
        </>
    )
}

export default Result;