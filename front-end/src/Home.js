/* eslint-disable no-useless-constructor */
import {Component} from 'react'
import './home.css';
import { Card } from 'antd';
import {
    HashRouter  as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

export default class Home extends Component{

    constructor(props){
        super(props)
    }
    render(){
        return(
            <div>
                <section id="banner">
                  <div className="inner">
                    <div className="logo"></div>
                    <p>
                    COMP90024 - Cluster and Cloud Computing <br />
                    Assignment Two <br />
                    </p>
                    <p>
                        <Link to="/app">Explore More</Link>
                    </p>
                </div>
                </section>
            </div>
        )
    }
}