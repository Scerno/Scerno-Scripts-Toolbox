// SPDX-License-Identifier: Unlicense
// Derived from https://github.com/Scerno/zonefile-extract.
// Run in the developer console on your own legacy 123-reg Advanced DNS page.
// Prints the visible records with a default TTL of 14400. See README.md.
(() => {
    const table = document.querySelector('.advanced_dns');
    if (!table) {
        throw new Error('The legacy 123-reg Advanced DNS table could not be found.');
    }

    const defaultTtl = '14400';
    const lines = [`$TTL ${defaultTtl}`];
    for (const row of table.querySelectorAll('tr')) {
        const name = row.querySelector('.dns_hostname');
        const type = row.querySelector('.dns_type');
        const ttl = row.querySelector('.dns_ttl');
        const priority = row.querySelector('.dns_priority');
        const data = row.querySelector('.dns_data');
        if (!name || !type || !data) continue;

        const recordType = type.innerText.trim();
        if (!recordType) continue;
        const destination = data.title;
        if (/[\r\n]/.test(destination)) {
            throw new Error('A record contains a multiline value. Review it manually.');
        }
        const isText = recordType === 'TXT/SPF';
        const value = isText
            ? '"' + destination.replaceAll('\\', '\\\\').replaceAll('"', '\\"') + '"'
            : destination;
        lines.push([
            name.innerText.trim() || '@',
            ttl?.innerText.trim() || defaultTtl,
            'IN',
            isText ? 'TXT' : recordType,
            priority?.innerText.trim(),
            value,
        ].filter(Boolean).join(' '));
    }
    if (lines.length === 1) {
        throw new Error('No recognizable DNS records were found.');
    }
    console.log(lines.join('\n'));
})();
