<<<<<<< HEAD
import React from 'react'

import classes from "./QuizTestRounds.module.css"



// <i className="fas fa-chevron-right"></i>

function QuizTestRounds( props ) {
    return (
        <div className = { classes.QuizTestRounds }>
            { props.symbol === "?" ? <i className="fas fa-question"></i> : <i className="fas fa-chevron-right"></i>}
            
        </div>
    )
}

export default QuizTestRounds
=======
import React from 'react'

import classes from "./QuizTestRounds.module.css"



// <i className="fas fa-chevron-right"></i>

function QuizTestRounds( props ) {
    return (
        <div className = { classes.QuizTestRounds }>
            { props.symbol === "?" ? <i className="fas fa-question"></i> : <i className="fas fa-chevron-right"></i>}
            
        </div>
    )
}

export default QuizTestRounds
>>>>>>> e7076219504e8160ea612f6d33d0aa7ef3418866
