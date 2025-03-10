async function write(string) {
    for (let i = 0; i < string.length; i++) {
        title.innerHTML = string.slice(0, i + 1);
        await new Promise(r => setTimeout(r, 100));
    }
    await new Promise(r => setTimeout(r, 5000));
    for (let i = title.innerHTML.length; i >= 0; i--) {
        title.innerHTML = title.innerHTML.slice(0, -1);
        await new Promise(r => setTimeout(r, 50));
    }
}

async function title() {
    const title = document.getElementById('name');

    const strings = ["South East Queensland Worst Running Club", "Your local running club", "Your gateway to start your running journey", "A vibrant community", "The worst running club in South East Queenland", "South East Queenslands Worst Running Club"]
    while (true) {

        // 1st: South East Queensland Worst Running Club
        var string = strings[0];
        for (let i = 0; i < string.length; i++) {
            title.innerHTML = string.slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 3000));
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));

        // 2nd: Your local running club
        var string = strings[1];
        for (let i = 0; i < string.length; i++) {
            title.innerHTML = string.slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 3000));
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));

        // 3rd: Your gateway to start your running journey
        var string = strings[2];
        for (let i = 0; i < string.length; i++) {
            title.innerHTML = string.slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 3000));
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));
        
        // 4th: a Vibrant community
        var string = strings[3];
        for (let i = 0; i < string.length; i++) {
            title.innerHTML = string.slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 3000));
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));

        // 5th: The worst running club in South East Queenland
        var string = strings[4];
        for (let i = 0; i < string.length; i++) {
            title.innerHTML = string.slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 3000));
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));

        // 6th: South East Queenslands Worst Running Club
        var string = strings[5];
        for (let i = 0; i < string.length; i++) {
            title.innerHTML = string.slice(0, i + 1);
            await new Promise(r => setTimeout(r, 100));
        }
        await new Promise(r => setTimeout(r, 3000));
        for (let i = title.innerHTML.length; i >= 0; i--) {
            title.innerHTML = title.innerHTML.slice(0, -1);
            await new Promise(r => setTimeout(r, 50));
        }
        await new Promise(r => setTimeout(r, 1000));
    }
}


title();