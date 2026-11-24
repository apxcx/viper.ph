---
title: OpenAI, Cisco Debut Shirudo for Linux
slug: shirudo-linux-security
date: '2026-11-24T08:00:00+08:00'
author: Viper Editorial Team
categories:
- AI
publisher_status: published
publication_slot: '08:00'
focus_keyword: Shirudo Linux security
seo_title: Shirudo Linux Security Runtime | Viper
seo_description: OpenAI and Cisco launched Shirudo, an open-source Linux runtime that uses eBPF shields to protect live systems while permanent patches are prepared.
canonical_url: https://viper.ph/shirudo-linux-security/
featured_image_key: articles/2026/11/shirudo-linux-security/featured.webp
featured_image_url: https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/featured.webp?v=202611240856
featured_image_alt: Shirudo logo with OpenAI and Cisco branding for the open-source Linux security runtime
featured_image_license: User-supplied, rights cleared
featured_image_credit: Provided by Viper editorial
featured_image_width: 2048
featured_image_height: 1152
sources:
- title: OpenAI and Cisco introduce Shirudo
  url: https://openai.com/index/introducing-shirudo/
  publisher: OpenAI
- title: Cisco and OpenAI Launch Shirudo, A New Project to Safeguard Agentic AI
  url: https://newsroom.cisco.com/content/c/r/newsroom/en/us/a/y2026/m11/cisco-and-openai-launch-shirudo-a-new-project-to-safeguard-agentic-ai.html
  publisher: Cisco
images:
- url: https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-1.webp?v=202611240856
  alt: Shirudo logo with OpenAI and Cisco branding for live Linux runtime protection
  source_url: https://viper.ph/shirudo-linux-security/
  credit: Provided by Viper editorial
  license: User-supplied, rights cleared
  rights_cleared: true
  width: 2048
  height: 1152
- url: https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-2.webp?v=202611240856
  alt: OpenAI Frontier visual representing the AI systems Shirudo is designed to protect
  source_url: https://viper.ph/shirudo-linux-security/
  credit: Provided by Viper editorial
  license: User-supplied, rights cleared
  rights_cleared: true
  width: 800
  height: 450
- url: https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-3.webp?v=202611240856
  alt: Security organizations supporting the broader Shirudo and open-source defense ecosystem
  source_url: https://viper.ph/shirudo-linux-security/
  credit: Provided by Viper editorial
  license: User-supplied, rights cleared
  rights_cleared: true
  width: 2048
  height: 1152
- url: https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-4.webp?v=202611240800
  alt: Linux infrastructure protection concept for the Shirudo agentic security project
  source_url: https://openai.com/index/introducing-shirudo/
  credit: OpenAI
  license: Official OpenAI newsroom image used with source credit for editorial context
  rights_cleared: true
  width: 1600
  height: 900
---
OpenAI and Cisco introduced Shirudo, an open-source runtime designed to help teams protect Linux systems while they prepare and deploy permanent patches. OpenAI said the project can use targeted eBPF shields to block vulnerable behavior on a running service without requiring a reboot. The announcement frames Shirudo as a response to a common security gap: patching can take time, but taking a production system offline may be unacceptable. For infrastructure operators, the idea is temporary, controlled protection that reduces exposure while normal maintenance continues.

![Shirudo logo with OpenAI and Cisco branding for live Linux runtime protection](https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-1.webp?v=202611240856)

Shirudo’s central mechanism is an eBPF program attached to a defined point in the Linux operating system. Security teams can test a proposed shield in observation mode, assess how it affects legitimate traffic, and then approve it for enforcement. OpenAI described a controlled test in which a Codex-generated shield blocked a Java4Shell exploit attempt against a running Elasticsearch service. The service continued operating while the malicious input was rejected. That demonstration is a test, not a guarantee that every vulnerability can be contained safely the same way.

![OpenAI Frontier visual representing the AI systems Shirudo is designed to protect](https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-2.webp?v=202611240856)

The project is built around several controls intended to keep machine-speed defense from becoming uncontrolled machine-speed change. Shields are cryptographically signed, checked by Linux’s eBPF verifier, and restricted by kernel security controls. Shirudo also uses a Trusted Platform Module to support a verifiable record of protections being loaded or removed. Those features matter because a temporary defense still changes behavior inside a live system. Operators need to know what was deployed, who approved it, and whether the protection can be audited after an incident.

![Security organizations supporting the broader Shirudo and open-source defense ecosystem](https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-3.webp?v=202611240856)

OpenAI and Cisco are releasing Shirudo under the BSD 2-Clause license, with its BPF programs dual-licensed under BSD and GPL, and are inviting developers and security researchers to inspect the code. The longer-term goal is an infrastructure layer that can identify affected systems, test targeted protections, and help operators contain compromises without disrupting workloads. Adoption will still depend on careful review, compatibility testing, and human approval. In practice, Shirudo is best understood as an open security project and experimental runtime, not an automatic replacement for patch management.

![Linux infrastructure protection concept for the Shirudo agentic security project](https://viper.ph/api/media/articles/2026/11/shirudo-linux-security/image-4.webp?v=202611240800)
