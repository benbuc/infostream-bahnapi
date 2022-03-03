import React from 'react';

import axios from 'axios';
import { Box, Button, Card, CardActions, CardContent, CardHeader, CircularProgress, Container, Grid, Typography } from '@mui/material';
import moment from 'moment';

export const isDev = () => !process.env.NODE_ENV || process.env.NODE_ENV === 'development';

interface IProps {

}
interface IState {
    stations: [];
    last_update: Date;
    loading: Boolean;
}

class Stations extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);

        this.state = {
            stations: [],
            last_update: new Date(0),
            loading: false,
        };
    }
    intervalId: NodeJS.Timer;

    componentDidMount() {

        this.intervalId = setInterval(() => { this.reloadData() }, 20000);
        this.reloadData();
    }

    componentWillUnmount() {
        clearInterval(this.intervalId);
    }

    reloadData = () => {
        this.setState({ loading: true });
        axios.get(isDev() ? "http://localhost:8000/" : "https://infostreamapi.benbuc.de")
            .then(res => {
                const stations = res.data['all_arrivals'];
                const last_update = new Date(res.data['last_update']);
                this.setState({ stations, last_update, loading: false });
            })
    }

    render() {
        const primary_loading_indicator = () => {
            if (this.state.loading && this.state.stations.length == 0) {
                return <CircularProgress />
            }
        }
        return (
            <Container maxWidth="md" component="main">
                <Typography>Last Update: {moment(this.state.last_update).format("DD.MM.YYYY HH:mm:ss")}</Typography>
                {primary_loading_indicator()}
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
                                        const estimated = new Date(arrival["estimated"])
                                        const eststring = moment(estimated).format("HH:mm")
                                        const schedstring = moment(arrival["scheduled"]).format("HH:mm")
                                        const delay = arrival["delay"] / 60;
                                        var datelabel = <Typography color={"#4caf50"}>{schedstring}</Typography>
                                        if (delay > 0 && delay <= 5) {
                                            datelabel = <Typography color={"#fcaf50"}>{schedstring} - {eststring} (+{delay})</Typography>
                                        } else if (delay > 5) {
                                            datelabel = <Typography color={"#ff5722"}>{schedstring} - {eststring} (+{delay})</Typography>
                                        }
                                        return (
                                            <Box paddingBottom={1}>
                                                <Typography>{arrival["name"]}</Typography>
                                                <Typography>{datelabel}</Typography>
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

export default Stations