function lineplot(ctx, x, train_data, valid_data, title="plot") {
    var chart = new Chart(ctx, {
    type: 'line',
    // The data for our dataset
    data: {
        labels: x,
        datasets: [
            {
                label: "train",
                backgroundColor: "#FF4F40",
                borderColor: "#FF4F40",
                data: train_data,
                fill: false,
            },{
                label: "valid",
                backgroundColor: "#307EC7",
                borderColor: "#307EC7",
                data: valid_data,
                fill: false,
            }
        ], // end of datasets list
    },
    // Disable animations to make it use less CPU
    options: {
        title: {
            text: title,
            display: true,
            position: "top",
            fontSize: 15,
            fontColor: "#666",
        },
        legend : {
            display: true,
            position: "bottom",
        },
        animation: {
            duration: 0, // general animation time
        },
        hover: {
            animationDuration: 0, // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
    }
    });
    return chart;
};
