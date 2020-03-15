<<<<<<< HEAD
import React from 'react'
import classes from "./MainPageContent.module.css"

import Quiz from "../../components/Quiz/Quiz"

import {Container, Row } from "react-bootstrap"

function MainPageContent() {
    return (
        <Container>
            <Row >
                <div className = { `${classes.MainPageContent} ${classes.wrapper}` }>
                    <Quiz />   

                </div>
            </Row>
        </Container>
    )
}

export default MainPageContent
=======
import React from 'react'
import classes from "./MainPageContent.module.css"

import Quiz from "../../components/Quiz/Quiz"

import {Container, Row } from "react-bootstrap"

function MainPageContent() {
    return (
        <Container>
            <Row >
                <div className = { `${classes.MainPageContent} ${classes.wrapper}` }>
                    <Quiz />   

                </div>
            </Row>
        </Container>
    )
}

export default MainPageContent
>>>>>>> e7076219504e8160ea612f6d33d0aa7ef3418866
