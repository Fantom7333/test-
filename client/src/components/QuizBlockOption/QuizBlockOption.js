import React from 'react'

import classes from "./QuizBlockOption.module.css"

function QuizBlockOption( props ) {
    return (
        <div className = { classes.QuizBlockOption }>
            <p>{ props.option }</p>
        </div>
    )
}

export default QuizBlockOption
