var controller = new ScrollMagic.Controller({
    globalSceneOptions: { duration: 740, triggerHook: 0.5 },
});
new ScrollMagic.Scene({ triggerElement: "#home" })
    .setClassToggle("#n1", "act")
    .addTo(controller);
new ScrollMagic.Scene({ triggerElement: "#about" })
    .setClassToggle("#n2", "act")
    .addTo(controller);
new ScrollMagic.Scene({ triggerElement: "#project" })
    .setClassToggle("#n3", "act")
    .addTo(controller);
new ScrollMagic.Scene({ triggerElement: "#contact" })
    .setClassToggle("#n4", "act")
    .addTo(controller);