/* eslint-disable no-useless-constructor */
import {Component} from 'react'

export default class Home extends Component{

    constructor(props){
        super(props)
    }
    render(){
        return(
            <div>
                123
            {/* <template>
            <div id="home" v-if="this.$route.path == '/'">
                <section id="banner">
                <div class="inner">
                    <div class="logo"></div>
                    <p>
                    COMP90024 - Cluster and Cloud Computing <br />
                    Assignment Two
                    </p>
                </div>
                <a href="#intro" class="more">Learn More</a>    
                </section>
                <section id="intro" class="wrapper center">
                <div class="inner">
                    <h2>Group Member</h2>
                    <p>Hanxun Huang - 975781</p>
                    <p>Haonan Chen - 930614</p>
                    <p>Lihuan Zhang - 945003</p>
                    <p>Xu Wang - 979895</p>
                    <p>Yang Xu- 961717</p>
                    <p class="button premium" onclick="window.location.href='/map'">
                    <a id='premium'>Go Premium</a>
                    </p>
                </div>
                </section>
            </div>
            </template> */}
            </div>
        )
    }
}