/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
// PNG in plaats van de standaard JPEG: de tussenframes gaan zonder verlies naar
// de encoder. Bij de fijne tekst in de taskpane en de offerte is dat zichtbaar
// scherper.
Config.setVideoImageFormat("png");
// Lagere CRF = hogere bitrate. 16 houdt de dunne lijnen en kleine cijfers heel.
Config.setCrf(16);
Config.setOverwriteOutput(true);
