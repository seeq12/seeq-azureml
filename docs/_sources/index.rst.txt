..
    seeq-azureml documentation master file, created manually.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to seeq-azureml's documentation
============================================

.. raw:: html

    <div style="background-color: #FFF8C5; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); padding: 10px">
        <div style="color: black; margin: 10px 10px 10px 10px">
            <b>Important Note:</b>
            <p>
                The seeq-azureml add-on is meant to be used for proof-of-concept models only. There are four significant caveats that users should be aware of when using this add-on:
            </p>
            <ol type="1">
              <li>A new Azure app registration must be set up to provide the identity to Seeq via OIDC (Open ID Connect).</li>
              <li>The Azure app registration needs contributor access to the AzureML Studio workspace.</li>
              <li>A secret needs to be generated and configured in an ini file as per the instructions on the Seeq Add-on Installation section of the documentation.</li>
              <li>This add-on has very limited capability for scalability to multiple assets.</li>
            </ol>
        </div>
    </div>
    <br>

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Introduction <introduction/introduction.md>
   Installation <installation/installation.md>
   User Guide <user_guide/user_guide.md>
   Code Documentation <code_documentation/index.rst>
   Changelog <changelog/changelog.md>
   License <license/license.md>
   Citation <citation/citation.md>
   View on GitHub <view_on_github/github.md>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


