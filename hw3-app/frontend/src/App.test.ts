import { expect, test } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import App from './App.svelte';




test('App', async () => {
  render(App);
});


test("Date is Current", async () => {
    render(App);

    const utcTime = new Date();
    const settings = {
        weekday: 'long' as 'long',
        year: 'numeric' as 'numeric',
        month: 'long' as 'long',
        day: 'numeric' as 'numeric',
    };
    const expectedDate = utcTime.toLocaleDateString('en-US', settings);
    const dateElement = screen.findByText(expectedDate);
    if (!dateElement) {
        throw new Error();
    }
});


test("API Key Retrieved", async () => {
    render(App);

    const res = await fetch('/api/key');
    const data = await res.json();
    const apiKey = data.apiKey;

    if (!apiKey) {
        throw new Error();
    }
});


test('Fake article content is displayed', async () => {
        const artTitle = ['TITLE', 'TITLE', 'TITLE'];
        const artAbstract = ['ABSTRACT', 'ABSTRACT', 'ABSTRACT'];
        const artImage= ['IMAGE', 'IMAGE', 'IMAGE'];
        const artCaption = ['CAPTION', 'CAPTION', 'CAPTION'];
    render(App, {
        props: {
            artTitle,
            artAbstract,
            artImage,
            artCaption,
        },
    });

    artTitle.forEach((title) => {
        const titleElement = screen.findByText(title);
        if(!titleElement){
            throw new Error();
        }
    });
    artAbstract.forEach((abstract) => {
        const abstractElement = screen.findByText(abstract);
        if(!abstractElement){
            throw new Error();
        }
    });
    artImage.forEach((image) => {
        const imageElement = screen.findByText(image);
        if(!imageElement){
            throw new Error();
        }
    });
    artCaption.forEach((caption) => {
        const captionElement = screen.findByText(caption);
        if(!captionElement){
            throw new Error();
        }
    });
});


test("Check for NYT API Correctness", async () => {
    // use the api key to query the nyt api
    // compare the data received with the expected format
    render(App);

    const url = `https://api.nytimes.com/svc/search/v2/articlesearch.json?q="Davis CA""U.C. Davis"&api-key=${App.apiKey}`;
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json",
        },
    };
    const response = await fetch(url, options);
    const data = await response.json();

    if (!data.response.docs[0].headline ||
            !data.response.docs[0].abstract ||
            !data.response.docs[0].multimedia.default.url ||
            !data.response.docs[0].multimedia.caption) {
        throw new Error();
    }
});


test("Screen sizing responsiveness", async () => {
    render(App);

    window.innerWidth = 400;
    const container = document.querySelector('.container');;
    if (!container) {
        throw new Error();
    }

    const phoneScreen = getComputedStyle(container);
    console.log('gridTemplateColumns:', phoneScreen.gridTemplateColumns);
    if (!phoneScreen.gridTemplateColumns.includes('auto')) {
        throw new Error();
    }
    
    window.innerWidth = 1000;
    const tabletScreen = getComputedStyle(container);
    if (!tabletScreen.gridTemplateColumns.includes('auto auto')) {
        throw new Error();
    }
    window.innerWidth = 2000;
    const laptopScreen = getComputedStyle(container);
    console.log('gridTemplateColumns:', laptopScreen.gridTemplateColumns);
    if (!laptopScreen.gridTemplateColumns.includes('auto auto auto')) {
        throw new Error();
    }
});