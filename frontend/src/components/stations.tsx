import React from 'react';

import axios from 'axios';
import { Box, Button, Card, CardActions, CardContent, CardHeader, Container, Grid, Typography } from '@mui/material';
import moment from 'moment';

interface IProps {

}
interface IState {
    stations: [];
}

class Stations extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);

        this.state = {
            stations: []
        };
    }

    componentDidMount() {
        axios.get(`http://localhost:8000`)
            .then(res => {
                const stations = res.data;
                //console.log(stations);
                this.setState({ stations });
            })
    }

    render() {
        this.state.stations.forEach(station => {
            console.log(station);
            console.log(station['station_name']);
            Object.keys(station['arrivals']).forEach((key) => {
                console.log(key);
            })
        });
        return (
            <Container maxWidth="md" component="main">
                <Grid container spacing={5} alignItems="flex-start">
                    {this.state.stations.map((station) => (
                        <Grid item
                            key={station["station_name"]}
                            xs={12}
                            sm={12}
                            md={4}
                        >
                            <Card>
                                <CardHeader
                                    title={station["station_name"]}
                                    subheader="Arrivals next 15 minutes"
                                />
                                <CardContent>
                                    {Object.keys(station["arrivals"]).map((key) => {
                                        const arrival = station["arrivals"][key]
                                        var dateString = "";
                                        if (arrival["estimated"]) {
                                            const estimated = new Date(arrival["estimated"])
                                            dateString = " @ " + moment(estimated).format("hh:mm")
                                        }
                                        return (
                                            <Box paddingBottom={1}>
                                                <p>{arrival["name"]}{dateString}</p>
                                                <p>Sched: {moment(arrival["scheduled"]).format("hh:mm")}</p>
                                            </Box>
                                        )
                                    })}
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        )
    }
}

/*<ul>
                {this.state.stations.map((station) => (
                    <li>{station["station_name"]}</li>
                ))}
            </ul>*/

export default Stations