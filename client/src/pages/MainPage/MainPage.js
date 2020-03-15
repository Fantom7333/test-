import React, { Component } from 'react'

import classes from "./MainPage.module.css"

import NavBar  from "../../components/UI/NavBar/NavBar"
import MainPageContent from "../../components/MainPageContent/MainPageContent"

export default class MainPage extends Component {
    render() {
        return (
            <div className = { classes.MainPage }>
                <NavBar />
                <MainPageContent />
            </div>
        )
    }
}
