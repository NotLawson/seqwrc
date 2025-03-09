async function title() {
    const title = document.getElementById('name');

    const strings = ["Your local running club", "The best", "The worst running club in South East Queenland", "South East Queenslands Worst Running Club"]

    while (true) {
        await new Promise(r => setTimeout(r, 1000));
        // backspacing
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        // typing
        // Your local running club
        await new Promise(r => setTimeout(r, 500));
        for (let i = 0; i < strings[0].length; i++) {
            title.innerHTML = strings[0].slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 5000));
        // backspacing
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }

        // typing
        // The best
        await new Promise(r => setTimeout(r, 500));
        for (let i = 0; i < strings[1].length; i++) {
            title.innerHTML = strings[1].slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        // backspacing
        for (let i = 4; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));

        // typing
        // the worst running club in South East Queenland
        await new Promise(r => setTimeout(r, 500));
        for (let i = 0; i < strings[2].length; i++) {
            title.innerHTML = strings[2].slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        // backspacing
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
    }
}

title();