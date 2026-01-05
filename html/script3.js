const waterAudio = new Audio('./water.mp3');
waterAudio.volume = 0.2
const walkAudio = new Audio('./walk.mp3');
const flowersAudio = new Audio('./flower.mp3');
const sounds = {
    walk: walkAudio,
    flowers: flowersAudio,
    water: waterAudio,
}

function throttle(callback, wait, immediate = false) {
    let timeout = null
    let initialCall = true
    return function() {
        const callNow = immediate && initialCall
        const next = () => {
            callback.apply(this, arguments)
            timeout = null
        }
        if (callNow) {
            initialCall = false
            next()
        }

        if (!timeout) {
            timeout = setTimeout(next, wait)
        }
    }
}

const showDefault = () => {
    Object.entries(sounds).forEach(([name, audio]) => {
        audio.pause()
    })
    document.querySelectorAll("iframe").forEach(iframe => {
        if (iframe.className === "default") {
            iframe.style.display = "block"
        } else {
            iframe.style.display = "none"
        }
    })
}

const scaleVideos = () => {
    const videoRatio = 218/387
    document.querySelectorAll(".video-wrapper").forEach(container => {
        container.querySelectorAll("iframe").forEach(iframe => {
            container.style.transform = "scale(1,1)"
            const containerRatio = container.offsetHeight / container.offsetWidth
            if (containerRatio > videoRatio) {
                const finalHeight = container.offsetHeight
                const finalWidth = finalHeight / videoRatio
                iframe.style["min-width"] = finalWidth + "px"
                iframe.style["min-height"] = finalHeight + "px"
            } else {
                const finalWidth = container.offsetWidth
                const finalHeight = finalWidth / videoRatio
                iframe.style["min-width"] = finalWidth + "px"
                iframe.style["min-height"] = finalHeight + "px"
            }
        })
    })
}
let videos = Array.from(document.querySelectorAll(".video-wrapper"))
const attachListener = () => {
    document.querySelector(".scrim").style.display = "none"
    document.querySelectorAll(".video-wrapper").forEach(wrapper => {
        const quadrant = wrapper.dataset.quadrant
        const type = wrapper.dataset.type
        wrapper.addEventListener("mouseenter", () => {
            videos = [wrapper].concat(videos.filter(v => v !== wrapper))
            videos.forEach((v, i) => v.style["z-index"] = 3 - i)
            Object.entries(sounds).forEach(([name, audio]) => {
                if (name === type) {
                    audio.play()
                } else {
                    audio.pause()
                }
            })
            document.querySelectorAll("iframe").forEach(iframe => {
                const iframeType = iframe.dataset.type
                console.log(iframeType, type)
                if(iframeType === type) {
                    iframe.style.display = "block"
                } else {
                    iframe.style.display = "none"
                }
            })
        })
        wrapper.addEventListener("mousemove", throttle((e) => {
            if (window.timer){
                clearTimeout(window.timer)
            }
            window.timer = setTimeout(showDefault, 10000)
            const box = wrapper.getBoundingClientRect()
            let pctX, pctY
            if (quadrant === "ul") {
                pctX = 1 - (e.clientX / box.width)
                pctY = 1 - (e.clientY / box.height)
            } else if (quadrant === "ur") {
                pctX = (e.clientX - box.x) / box.width
                pctY = 1 - (e.clientY / box.height)
            } else if (quadrant === "ll") {
                pctX = 1 - (e.clientX / box.width)
                pctY = (e.clientY - box.y) / box.height
            } else if (quadrant === "lr") {
                pctX = (e.clientX - box.x) / box.width
                pctY = (e.clientY - box.y) / box.height
            }
            wrapper.style.transform = `scale(${1+(pctX * 1)}, ${1 + (pctY * 1)})`
            e.preventDefault()
        }, 50))
    })
}

scaleVideos()
let dismissed = false
var fsElem = document.documentElement;
document.querySelector(".scrim").addEventListener("click", () => {
    if(!dismissed){
        document.querySelector(".scrim").style.opacity = 0;
        setTimeout(() => {
            attachListener();
        },10000)
        dismissed = true
        document.getElementsByTagName('html')[0].style.cursor = 'none'
        fsElem.requestFullscreen();
    }
})

setTimeout(()=>{
//    document.querySelector(".scrim").click();
}, 100);

