const intro = introJs();

intro.setOptions({
    steps: [
        {
            element: '#navbar',
            intro: 'This is the navbar. It contains links to all the pages you can visit.',
        },
    ]
})

document.getElementById('start-steps').addEventListener('click', function(){
    intro.start();
})